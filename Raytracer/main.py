from dataclasses import dataclass, field
import math
import random
import torch


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


class TensorizedGeometry:
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


@dataclass
class TensorizedRays:
    n_rays: int
    ray_times: torch.Tensor
    ray_positions: torch.Tensor
    ray_velocities: torch.Tensor


def generate_tensorized_rays(n_rays: int, device: torch.device) -> TensorizedRays:
    return TensorizedRays(
        n_rays = n_rays,
        ray_times = torch.zeros((n_rays,), device=device),
        ray_positions = torch.rand((n_rays, 3), device=device) * 8 + 1,
        ray_velocities = torch.rand((n_rays, 3), device=device) * 2 - 1,
    )


def intersect_rays(
    r: TensorizedRays,
    g: TensorizedGeometry,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Return the following for each ray in the scene:
        - time to intersection
        - index of intersected face
        - normal vector of intersected face
    Negative times indicate no intersection.
    """
    hit_times = torch.full((r.ray_positions.size(0),), -1.0, device=r.ray_positions.device)  # 0.03 ms
    closest_normals = torch.zeros_like(r.ray_positions)  # 0.004 ms

    # how long does it take each ray to intersect each face?
    ray_v_perp_faces = torch.matmul(r.ray_velocities, g.face_normals)  # 26 ms
    ray_d_perp_faces = g.face_d_origins - torch.matmul(r.ray_positions, g.face_normals)  # 30 ms
    ray_dt_faces = ray_d_perp_faces / ray_v_perp_faces  # 0.27 ms

    # where would each ray intersect each face?
    invalid_mask = (ray_v_perp_faces != 0) * (ray_dt_faces > 0)  # 0.89 ms
    ray_dt_faces = ray_dt_faces * invalid_mask  # 0.29 ms - no need to calculate non-intersections
    ray_final_positions = (  # 0.61 ms
        r.ray_positions.unsqueeze(2) +
        r.ray_velocities.unsqueeze(2) * ray_dt_faces.unsqueeze(1)
    )

    # 6.3 ms
    # check if intersection points are inside the face
    ray_final_as = torch.einsum("ijk,jk->ik", ray_final_positions, g.face_a_vecs)  # 0.09 ms
    ray_final_bs = torch.einsum("ijk,jk->ik", ray_final_positions, g.face_b_vecs)  # 0.09 ms
    invalid_mask *= (  # 120 ms
        (ray_final_as >= g.face_a_mins) &
        (ray_final_as <= g.face_a_maxes) &
        (ray_final_bs >= g.face_b_mins) &
        (ray_final_bs <= g.face_b_maxes)
    )

    # 16.5 ms
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


def raytrace_event(
    geometry: TensorizedGeometry,
    rays: TensorizedRays,
    device: torch.device,
) -> tuple[int, torch.Tensor, torch.Tensor, torch.Tensor]:
    # 0.73 ms
    absorption_indices = torch.full((rays.n_rays,), -2, device=device)  # -2 = in flight, -1 = lost
    absorption_times = torch.full((rays.n_rays,), -1.0, device=device)
    done_mask = torch.full((rays.n_rays,), True, device=device)
    max_bounces = 100

    # 87 ms per loop - aim for 50 ms
    for bounce in range(max_bounces):
        # 0.2 ms
        n_photons_remaining = int(torch.sum(done_mask).item())
        if not n_photons_remaining:
            break

        # 37 ms
        print("Intersecting rays")
        hit_times, closest_indices, closest_normals = intersect_rays(rays, geometry)

        # 0.15 ms
        # rays that hit an absorber or nothing are lost
        absorbed_mask = torch.rand(n_photons_remaining, device=device) < geometry.face_reflectivities[closest_indices]
        lost_mask = hit_times > 0
        new_mask = absorbed_mask * lost_mask

        # 2.2 ms
        # absorb rays
        new_absorbed_indices = torch.where(done_mask)[0][~absorbed_mask]
        absorption_indices[new_absorbed_indices] = closest_indices[~absorbed_mask]
        absorption_times[new_absorbed_indices] = rays.ray_times[~absorbed_mask]

        # 1.2 ms
        # lose rays
        unmasked_indices = torch.where(done_mask)[0]
        new_lost_indices = unmasked_indices[~lost_mask]
        absorption_indices[new_lost_indices] = -1

        # 4.7 ms
        # update full mask
        done_mask[unmasked_indices[~new_mask]] = False  # 0.8 ms
        rays.ray_positions = rays.ray_positions[new_mask]  # 0.8 ms
        rays.ray_velocities = rays.ray_velocities[new_mask]  # 0.8 ms
        rays.ray_times = rays.ray_times[new_mask]  # 0.8 ms
        hit_times = hit_times[new_mask]  # 0.8 ms
        closest_normals = closest_normals[new_mask]  # 0.8 ms

        # 0.08 ms
        # propagate rays
        rays.ray_positions += (
            rays.ray_velocities *
            (hit_times - 1e-5).unsqueeze(1)  # avoid tunneling
        )
        rays.ray_times += hit_times

        # 0.1 ms
        # reflect ray_velocities using face normals: R = V - 2 * (V · N) * N
        dot_product = torch.sum(
            rays.ray_velocities * closest_normals,
            dim=1,
            keepdim=True,
        )
        rays.ray_velocities -= 2 * dot_product * closest_normals

    return bounce, absorption_indices, absorption_times, done_mask  # type: ignore


def main():
    # do not use MPS! unreliable (wrong calculations) and slow
    device = torch.device(
        "cuda" if torch.cuda.is_available()
        else "cpu"
    )
    print(f"Using device: {device}")

    # populate scene
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
        RectElement(face=face, reflectivity=0.95)
        for face in wall_faces
    ] + [
        RectElement(face=face, reflectivity=0.0)
        for face in absorber_faces
    ]
    geometry = TensorizedGeometry(elements, device)

    # raytrace all events simultaneously
    n_rays_per_event = 30_000
    n_events = 1_000
    n_rays = n_rays_per_event * n_events

    # 1.5 ms
    rays = generate_tensorized_rays(n_rays, device)

    # 6.1 s
    print("ray tracing")
    bounce, absorption_indices, absorption_times, done_mask = raytrace_event(geometry, rays, device)

    # 11.8 ms
    print("absorbing")
    # fill absorption times
    for i, element in enumerate(elements):
        element.absorbed_times = absorption_times[absorption_indices == i].tolist()

    # results
    print(f"Simulation finished after {bounce + 1} bounces")  # type: ignore
    print("Absorption:")
    print("\n".join(
        f"\tFace {i}: {len(elements[i].absorbed_times)} absorbed rays"
        for i in range(len(elements))
    ))
    print(f"Lost rays: {torch.sum(absorption_indices == -1)}")
    print(f"Rays in flight: {torch.sum(done_mask)}")


if __name__ == "__main__":
    """
    How can I make this faster?
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

    # # torch profiler
    # # open Instruments > Metal System Trace > run script while recording
    # with torch.mps.profiler.profile(mode='interval'):
        # main()
