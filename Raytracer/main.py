from dataclasses import dataclass
import math
from random import random
import torch


"""
Terminology:
    - Face: a human-readable object with Euclidean coordinates and a tensor() function that returns a FaceTensor
    - FaceTensor: a dataclass of non-human-readable Tensors used in raytracing calculations
    - Element: a Face with reflectivity and a list of absorption times
"""


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


class RectFace:
    def tensor(self) -> "RectFaceTensor":
        raise NotImplementedError


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
        dtype = torch.float32
        return RectFaceTensor(
            normal=self.normal.to(device, dtype=dtype),
            d_origin=self.d_origin.to(device, dtype=dtype),
            in_plane_a=self.in_plane_a.to(device, dtype=dtype),
            a_min=self.a_min.to(device, dtype=dtype),
            a_max=self.a_max.to(device, dtype=dtype),
            in_plane_b=self.in_plane_b.to(device, dtype=dtype),
            b_min=self.b_min.to(device, dtype=dtype),
            b_max=self.b_max.to(device, dtype=dtype),
        )


@dataclass
class XRectFace(RectFace):
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
class YRectFace(RectFace):
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
class ZRectFace(RectFace):
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


def make_box_elements(
    x_min: float, x_max: float,
    y_min: float, y_max: float,
    z_min: float, z_max: float,
    reflectivity: float,
) -> list[RectElement]:
    """
    Make all RectElements for a box of given dimensions.
    """
    return [
        RectElement(
            face=box_face,
            reflectivity=reflectivity,
        )
        for box_face in [
            XRectFace(x_min, y_min, y_max, z_min, z_max),
            XRectFace(x_max, y_min, y_max, z_min, z_max),
            YRectFace(x_min, x_max, y_min, z_min, z_max),
            YRectFace(x_min, x_max, y_max, z_min, z_max),
            ZRectFace(x_min, x_max, y_min, y_max, z_min),
            ZRectFace(x_min, x_max, y_min, y_max, z_max),
        ]
    ]


class _TensorizedGeometry:
    def __init__(self, elements: list[RectElement], device: torch.device):
        face_tensors = [element.face.tensor().to(device) for element in elements]
        self.face_normals = torch.stack([face.normal for face in face_tensors], dim=1)
        self.face_d_origins = torch.stack([face.d_origin for face in face_tensors])
        self.face_a_vecs = torch.stack([face.in_plane_a for face in face_tensors], dim=1)
        self.face_a_mins = torch.stack([face.a_min for face in face_tensors])
        self.face_a_maxes = torch.stack([face.a_max for face in face_tensors])
        self.face_b_vecs = torch.stack([face.in_plane_b for face in face_tensors], dim=1)
        self.face_b_mins = torch.stack([face.b_min for face in face_tensors])
        self.face_b_maxes = torch.stack([face.b_max for face in face_tensors])
        self.face_reflectivities = torch.tensor(
            [element.reflectivity for element in elements],
            device=device,
        )


class _TensorizedRays:
    def __init__(self, rays: list[Ray], device: torch.device):
        self.n_rays = len(rays)
        dtype = torch.float32
        self.ray_times = torch.zeros((self.n_rays,), device=device, dtype=dtype)
        self.ray_positions = torch.tensor([[ray.position.x, ray.position.y, ray.position.z] for ray in rays], device=device, dtype=dtype)
        self.ray_velocities = torch.tensor([[ray.velocity.x, ray.velocity.y, ray.velocity.z] for ray in rays], device=device, dtype=dtype)


def _intersect_rays(
    r: _TensorizedRays,
    g: _TensorizedGeometry,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Return the following for each ray in the scene:
        - time to intersection
        - index of intersected face
        - normal vector of intersected face
    Negative times indicate no intersection.
    """
    hit_times = torch.full((r.ray_positions.size(0),), -1.0, device=r.ray_positions.device)
    closest_normals = torch.zeros_like(r.ray_positions)

    # how long does it take each ray to intersect each face?
    ray_v_perp_faces = torch.matmul(r.ray_velocities, g.face_normals)
    ray_d_perp_faces = g.face_d_origins - torch.matmul(r.ray_positions, g.face_normals)
    ray_dt_faces = ray_d_perp_faces / ray_v_perp_faces

    # where would each ray intersect each face?
    invalid_mask = (ray_v_perp_faces != 0) * (ray_dt_faces > 0)
    ray_dt_faces = ray_dt_faces * invalid_mask
    ray_final_positions = (
        r.ray_positions.unsqueeze(2) +
        r.ray_velocities.unsqueeze(2) * ray_dt_faces.unsqueeze(1)
    )

    # check if intersection points are inside the face
    ray_final_as = torch.einsum("ijk,jk->ik", ray_final_positions, g.face_a_vecs)
    as_in_bound = (ray_final_as >= g.face_a_mins) * (ray_final_as <= g.face_a_maxes)
    ray_final_bs = torch.einsum("ijk,jk->ik", ray_final_positions, g.face_b_vecs)
    bs_in_bound = (ray_final_bs >= g.face_b_mins) * (ray_final_bs <= g.face_b_maxes)
    invalid_mask *= as_in_bound * bs_in_bound

    # find closest intersections
    ray_dt_faces = torch.where(
        invalid_mask,
        ray_dt_faces,
        torch.tensor(float("inf"), device=ray_dt_faces.device),
    )
    closest_indices = torch.argmin(ray_dt_faces, dim=1)
    closest_normals = g.face_normals.t()[closest_indices]
    hit_times = ray_dt_faces[torch.arange(ray_dt_faces.size(0)), closest_indices]
    no_intersections = torch.all(~invalid_mask, dim=1)
    hit_times[no_intersections] = -1

    return hit_times, closest_indices, closest_normals


def intersect_rays(
    all_elements: list[RectElement],
    all_rays: list[Ray],
    device: torch.device,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    geometry = _TensorizedGeometry(all_elements, device)
    rays = _TensorizedRays(all_rays, device)
    hit_times, closest_indices, closest_normals = _intersect_rays(rays, geometry)
    return hit_times, closest_indices, closest_normals


def raytrace_event(
    all_elements: list[RectElement],
    all_rays: list[Ray],
    max_bounces: int,
    device: torch.device,
) -> tuple[torch.Tensor, torch.Tensor]:
    geometry = _TensorizedGeometry(all_elements, device)
    rays = _TensorizedRays(all_rays, device)

    absorption_indices = torch.full((rays.n_rays,), -2, device=device)  # -2 = in flight, -1 = lost
    absorption_times = torch.full((rays.n_rays,), -1.0, device=device)
    done_mask = torch.full((rays.n_rays,), True, device=device)

    for bounce_n in range(max_bounces):
        n_photons_remaining = int(torch.sum(done_mask).item())
        if not n_photons_remaining:
            break

        hit_times, closest_indices, closest_normals = _intersect_rays(rays, geometry)

        # propagate rays
        rays.ray_positions += (
            rays.ray_velocities *
            (hit_times - 1e-4).unsqueeze(1)  # epsilon difference to avoid tunneling
        )
        rays.ray_times += hit_times

        # reflect ray_velocities using face normals: R = V - 2 * (V · N) * N
        dot_product = torch.sum(
            rays.ray_velocities * closest_normals,
            dim=1,
            keepdim=True,
        )
        rays.ray_velocities -= 2 * dot_product * closest_normals

        # rays that hit an absorber or nothing are lost
        absorbed_mask = torch.rand(n_photons_remaining, device=device) < geometry.face_reflectivities[closest_indices]
        lost_mask = hit_times > 0
        new_mask = absorbed_mask * lost_mask

        # absorb rays
        new_absorbed_indices = torch.where(done_mask)[0][~absorbed_mask]
        absorption_indices[new_absorbed_indices] = closest_indices[~absorbed_mask]
        absorption_times[new_absorbed_indices] = rays.ray_times[~absorbed_mask]

        # lose rays
        unmasked_indices = torch.where(done_mask)[0]
        new_lost_indices = unmasked_indices[~lost_mask]
        absorption_indices[new_lost_indices] = -1

        # update full mask
        done_mask[unmasked_indices[~new_mask]] = False
        rays.ray_positions = rays.ray_positions[new_mask]
        rays.ray_velocities = rays.ray_velocities[new_mask]
        rays.ray_times = rays.ray_times[new_mask]
        hit_times = hit_times[new_mask]
        closest_normals = closest_normals[new_mask]

    return absorption_indices, absorption_times  # type: ignore


def main():
    # do not use MPS! unreliable (wrong calculations) and slow
    device = torch.device(
        "cuda" if torch.cuda.is_available()
        else "cpu"
    )
    print(f"Using device: {device}")

    # populate scene
    wall_faces = [
        XRectFace(x=0, y_min=0, y_max=10, z_min=0, z_max=10),
        XRectFace(x=10, y_min=0, y_max=10, z_min=0, z_max=10),
        YRectFace(x_min=0, x_max=10, y=0, z_min=0, z_max=10),
        YRectFace(x_min=0, x_max=10, y=10, z_min=0, z_max=10),
        ZRectFace(x_min=0, x_max=10, y_min=0, y_max=10, z=0),
        ZRectFace(x_min=0, x_max=10, y_min=0, y_max=10, z=10),
    ]
    absorber_faces = [
        XRectFace(x=4, y_min=4, y_max=6, z_min=4, z_max=6),
        XRectFace(x=6, y_min=4, y_max=6, z_min=4, z_max=6),
        YRectFace(x_min=4, x_max=6, y=4, z_min=4, z_max=6),
        YRectFace(x_min=4, x_max=6, y=6, z_min=4, z_max=6),
        ZRectFace(x_min=4, x_max=6, y_min=4, y_max=6, z=4),
        ZRectFace(x_min=4, x_max=6, y_min=4, y_max=6, z=6),
    ]
    elements = [
        RectElement(face=face, reflectivity=0.95)
        for face in wall_faces
    ] + [
        RectElement(face=face, reflectivity=0.0)
        for face in absorber_faces
    ]

    # raytrace
    n_rays_per_event = 30_000
    n_total_events = 10_000
    n_events_in_batch = 250
    n_rays_per_batch = n_rays_per_event * n_events_in_batch
    n_batches = n_total_events // n_events_in_batch
    max_bounces = 100

    for _ in range(n_batches):
        rays = [
            Ray(
                position = Vector(random()*8+1, random()*8+1, random()*8+1),
                velocity = Vector(random()*2-1, random()*2-1, random()*2-1),
            )
            for _ in range(n_rays_per_batch)
        ]
        absorption_indices, absorption_times = raytrace_event(elements, rays, max_bounces, device)
        absorption_times = [
            absorption_times[absorption_indices == i].tolist()
            for i, _ in enumerate(elements)
        ]


if __name__ == "__main__":
    """
    Optimized for an A100 GPU.
    """
    main()

    # # timing tests
    # import timeit
    # def my_function():
        # main()
    # n_trials = 10
    # execution_time = timeit.timeit(my_function, number=n_trials)
    # print(f"Execution time: {execution_time*1000/n_trials:.5f} ms")
    # breakpoint()
