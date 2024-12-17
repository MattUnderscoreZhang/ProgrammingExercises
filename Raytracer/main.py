from dataclasses import dataclass, field
import math
import random
import torch
from torch.backends import mps


@dataclass
class Vector:
    x: float
    y: float
    z: float

    def __mul__(self, other: float) -> "Vector":
        return Vector(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other: float) -> "Vector":
        return self.__mul__(other)

    def __truediv__(self, other: float) -> "Vector":
        return Vector(self.x / other, self.y / other, self.z / other)

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def length(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def tensor(self) -> torch.Tensor:
        return torch.tensor([self.x, self.y, self.z])


@dataclass
class Ray:
    position: Vector
    velocity: Vector


@dataclass
class RectFace:
    def tensor(self) -> "RectFaceTensor":
        raise NotImplementedError


@dataclass
class XRect(RectFace):
    x: float
    y_min: float
    y_max: float
    z_min: float
    z_max: float

    def tensor(self) -> 'RectFaceTensor':
        return RectFaceTensor(
            normal=torch.tensor([1.0, 0, 0]),
            d_origin=torch.tensor(self.x),
            in_plane_a=torch.tensor([0, 1.0, 0]),
            a_min=torch.tensor(self.y_min),
            a_max=torch.tensor(self.y_max),
            in_plane_b=torch.tensor([0, 0, 1.0]),
            b_min=torch.tensor(self.z_min),
            b_max=torch.tensor(self.z_max),
        )


@dataclass
class YRect(RectFace):
    x_min: float
    x_max: float
    y: float
    z_min: float
    z_max: float

    def tensor(self) -> 'RectFaceTensor':
        return RectFaceTensor(
            normal=torch.tensor([0, 1.0, 0]),
            d_origin=torch.tensor(self.y),
            in_plane_a=torch.tensor([1.0, 0, 0]),
            a_min=torch.tensor(self.x_min),
            a_max=torch.tensor(self.x_max),
            in_plane_b=torch.tensor([0, 0, 1.0]),
            b_min=torch.tensor(self.z_min),
            b_max=torch.tensor(self.z_max),
        )


@dataclass
class ZRect(RectFace):
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    z: float

    def tensor(self) -> 'RectFaceTensor':
        return RectFaceTensor(
            normal=torch.tensor([0, 0, 1.0]),
            d_origin=torch.tensor(self.z),
            in_plane_a=torch.tensor([0, 1.0, 0]),
            a_min=torch.tensor(self.y_min),
            a_max=torch.tensor(self.y_max),
            in_plane_b=torch.tensor([1.0, 0, 0]),
            b_min=torch.tensor(self.x_min),
            b_max=torch.tensor(self.x_max),
        )


@dataclass
class RectElement:
    face: RectFace
    reflectivity: float
    absorbed_times: list[float] = field(default_factory=list)


@dataclass
class RectFaceTensor:
    normal: torch.Tensor
    d_origin: torch.Tensor  # distance from origin to face, in the direction of the normal
    in_plane_a: torch.Tensor  # vector in the plane of the face
    a_min: torch.Tensor  # bounds for the vector
    a_max: torch.Tensor  # bounds for the vector
    in_plane_b: torch.Tensor
    b_min: torch.Tensor
    b_max: torch.Tensor

    def to(self, device: torch.device) -> 'RectFaceTensor':
        return RectFaceTensor(
            normal=self.normal.to(device),
            d_origin=self.d_origin.to(device),
            in_plane_a=self.in_plane_a.to(device),
            a_min=self.a_min.to(device),
            a_max=self.a_max.to(device),
            in_plane_b=self.in_plane_b.to(device),
            b_min=self.b_min.to(device),
            b_max=self.b_max.to(device),
        )


def intersect_rays(
    ray_positions: torch.Tensor,
    ray_velocities: torch.Tensor,
    face_normals: torch.Tensor,
    face_d_origins: torch.Tensor,
    face_a_vecs: torch.Tensor,
    face_a_mins: torch.Tensor,
    face_a_maxes: torch.Tensor,
    face_b_vecs: torch.Tensor,
    face_b_mins: torch.Tensor,
    face_b_maxes: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Return the following for each ray in the scene:
        - time to intersection
        - index of intersected face
        - normal vector of intersected face
    Negative times indicate no intersection.
    """
    intersection_times = torch.full(size=(ray_positions.size(0),), fill_value=-1.0, device=ray_positions.device)
    closest_normals = torch.zeros_like(ray_positions)

    # how long does it take each ray to intersect each face?
    ray_v_perp_faces = torch.matmul(ray_velocities, face_normals)
    invalid_mask = ray_v_perp_faces != 0
    ray_d_perp_faces = face_d_origins - torch.matmul(ray_positions, face_normals)
    ray_dt_faces = ray_d_perp_faces / ray_v_perp_faces

    # where would each ray intersect each face?
    invalid_mask &= (ray_dt_faces > 0)  # negative times indicate no intersection
    ray_dt_faces = ray_dt_faces * invalid_mask  # no need to calculate non-intersections
    ray_final_positions = (
        ray_positions.unsqueeze(2) +
        ray_velocities.unsqueeze(2) * ray_dt_faces.unsqueeze(1)
    )

    # check if intersection points are inside the face
    ray_final_as = torch.einsum("ijk,jk->ik", ray_final_positions, face_a_vecs)
    ray_final_bs = torch.einsum("ijk,jk->ik", ray_final_positions, face_b_vecs)
    within_bounds = (
        (ray_final_as >= face_a_mins) *
        (ray_final_as <= face_a_maxes) *
        (ray_final_bs >= face_b_mins) *
        (ray_final_bs <= face_b_maxes)
    )
    invalid_mask &= within_bounds

    # find closest intersections
    ray_dt_faces = torch.where(
        invalid_mask,
        ray_dt_faces,
        torch.tensor(float("inf"), device=ray_dt_faces.device),
    )
    closest_indices = torch.argmin(ray_dt_faces, dim=1)
    closest_normals = face_normals.t()[closest_indices]
    intersection_times = ray_dt_faces[torch.arange(ray_dt_faces.size(0)), closest_indices]
    no_intersections = torch.all(~invalid_mask, dim=1)
    intersection_times[no_intersections] = -1

    return intersection_times, closest_indices, closest_normals


def main():
    device = torch.device(
        "mps" if mps.is_built()
        else "cuda" if torch.cuda.is_available()
        else "cpu"
    )
    print(f"Using device: {device}")

    # populate scene
    n_rays = 30000
    rays = [
        Ray(
            position=Vector(*[random.random() * 10 for _ in range(3)]),
            velocity=Vector(*[random.random() * 2 - 1 for _ in range(3)])
        )
        for _ in range(n_rays)
    ]
    wall_faces = [
        XRect(x=0, y_min=0, y_max=10, z_min=0, z_max=10),
        XRect(x=10, y_min=0, y_max=10, z_min=0, z_max=10),
        YRect(x_min=0, x_max=10, y=0, z_min=0, z_max=10),
        YRect(x_min=0, x_max=10, y=10, z_min=0, z_max=10),
        ZRect(x_min=0, x_max=10, y_min=0, y_max=10, z=0),
        ZRect(x_min=0, x_max=10, y_min=0, y_max=10, z=10),
    ]
    absorber_faces = [
        XRect(x=4, y_min=4, y_max=6, z_min=4, z_max=6),
        XRect(x=6, y_min=4, y_max=6, z_min=4, z_max=6),
        YRect(x_min=4, x_max=6, y=4, z_min=4, z_max=6),
        YRect(x_min=4, x_max=6, y=6, z_min=4, z_max=6),
        ZRect(x_min=4, x_max=6, y_min=4, y_max=6, z=4),
        ZRect(x_min=4, x_max=6, y_min=4, y_max=6, z=6),
    ]
    elements = [
        RectElement(face=face, reflectivity=1.0)
        for face in wall_faces
    ] + [
        RectElement(face=face, reflectivity=0.0)
        for face in absorber_faces
    ]

    # transfer to GPU
    ray_times = torch.zeros(n_rays, device=device)
    ray_positions = torch.stack([ray.position.tensor() for ray in rays]).to(device)
    ray_velocities = torch.stack([ray.velocity.tensor() for ray in rays]).to(device)
    face_tensors = [element.face.tensor().to(device) for element in elements]
    face_normals = torch.stack([face.normal for face in face_tensors], dim=1)
    face_d_origins = torch.stack([face.d_origin for face in face_tensors])
    face_a_vecs = torch.stack([face.in_plane_a for face in face_tensors], dim=1)
    face_a_mins = torch.stack([face.a_min for face in face_tensors])
    face_a_maxes = torch.stack([face.a_max for face in face_tensors])
    face_b_vecs = torch.stack([face.in_plane_b for face in face_tensors], dim=1)
    face_b_mins = torch.stack([face.b_min for face in face_tensors])
    face_b_maxes = torch.stack([face.b_max for face in face_tensors])

    # raytracing loop
    max_bounces = 100
    for bounce in range(max_bounces):
        if len(ray_positions) == 0:
            break

        intersection_times, closest_indices, closest_normals = intersect_rays(
            ray_positions,
            ray_velocities,
            face_normals,
            face_d_origins,
            face_a_vecs,
            face_a_mins,
            face_a_maxes,
            face_b_vecs,
            face_b_mins,
            face_b_maxes,
        )

        # rays that hit nothing are lost
        hit_mask = intersection_times > 0
        ray_times = ray_times[hit_mask]
        ray_positions = ray_positions[hit_mask]
        ray_velocities = ray_velocities[hit_mask]
        intersection_times = intersection_times[hit_mask]
        closest_indices = closest_indices[hit_mask]
        closest_normals = closest_normals[hit_mask]

        # check whether rays absorb or reflect
        hit_reflectivities = torch.tensor(
            [elements[i].reflectivity for i in closest_indices],
            device=device,
        )
        does_absorb = torch.rand(int(hit_mask.sum()), device=device) > hit_reflectivities

        # propagate rays
        ray_positions += ray_velocities * intersection_times.unsqueeze(1)
        ray_times += intersection_times

        # absorb rays
        for i, hit_i in enumerate(closest_indices):
            if does_absorb[i]:
                elements[hit_i].absorbed_times.append(ray_times[i].item())
        ray_times = ray_times[~does_absorb]
        ray_positions = ray_positions[~does_absorb]
        ray_velocities = ray_velocities[~does_absorb]
        intersection_times = intersection_times[~does_absorb]
        closest_indices = closest_indices[~does_absorb]
        closest_normals = closest_normals[~does_absorb]

        # reflect ray_velocities using face normals: R = V - 2 * (V · N) * N
        dot_product = torch.sum(
            ray_velocities * closest_normals,
            dim=1,
            keepdim=True,
        )
        ray_velocities -= 2 * dot_product * closest_normals

    # results
    print(f"Simulation finished after {bounce + 1} bounces")
    print("Absorption:")
    print("\n".join(
        f"Face {i}: {len(elements[i].absorbed_times)} absorbed rays"
        for i in range(len(elements))
    ))


if __name__ == "__main__":
    main()
