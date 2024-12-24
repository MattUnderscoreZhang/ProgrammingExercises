from random import random
from main import raytrace_event, make_box_elements, XRectFace, YRectFace, ZRectFace, RectElement, Ray, Vector
import sys
import torch


def test_x_rect_hit():
    element = RectElement(
        face=XRectFace(x=0, y_min=0, y_max=1, z_min=0, z_max=1),
        reflectivity=0,
    )
    ray = Ray(
        position=Vector(-0.5, 0.5, 0.5),
        velocity=Vector(1, 0, 0),
    )
    absorption_indices, absorption_times = raytrace_event(all_elements=[element], all_rays=[ray], max_bounces=1, device=torch.device("cpu"))
    assert absorption_indices[0] == 0
    assert absorption_times[0] == 0.5


def test_x_rect_no_hit():
    # wrong direction
    element = RectElement(
        face=XRectFace(x=0, y_min=0, y_max=1, z_min=0, z_max=1),
        reflectivity=0,
    )
    ray = Ray(
        position=Vector(0.5, 0.5, 0.5),
        velocity=Vector(1, 0, 0),
    )
    absorption_indices, _ = raytrace_event(all_elements=[element], all_rays=[ray], max_bounces=1, device=torch.device("cpu"))
    assert absorption_indices[0] == -1

    # miss in y
    ray = Ray(
        position=Vector(-0.5, 1.5, 0.5),
        velocity=Vector(1, 0, 0),
    )
    absorption_indices, _ = raytrace_event(all_elements=[element], all_rays=[ray], max_bounces=1, device=torch.device("cpu"))
    assert absorption_indices[0] == -1

    # miss in z
    ray = Ray(
        position=Vector(-0.5, 0.5, 1.5),
        velocity=Vector(1, 0, 0),
    )
    absorption_indices, _ = raytrace_event(all_elements=[element], all_rays=[ray], max_bounces=1, device=torch.device("cpu"))
    assert absorption_indices[0] == -1


def test_y_rect_hit():
    element = RectElement(
        face=YRectFace(x_min=0, x_max=1, y=0, z_min=0, z_max=1),
        reflectivity=0,
    )
    ray = Ray(
        position=Vector(0.5, -0.5, 0.5),
        velocity=Vector(0, 1, 0),
    )
    absorption_indices, absorption_times = raytrace_event(all_elements=[element], all_rays=[ray], max_bounces=1, device=torch.device("cpu"))
    assert absorption_indices[0] == 0
    assert absorption_times[0] == 0.5


def test_y_rect_no_hit():
    # wrong direction
    element = RectElement(
        face=YRectFace(x_min=0, x_max=1, y=0, z_min=0, z_max=1),
        reflectivity=0,
    )
    ray = Ray(
        position=Vector(0.5, 0.5, 0.5),
        velocity=Vector(0, 1, 0),
    )
    absorption_indices, _ = raytrace_event(all_elements=[element], all_rays=[ray], max_bounces=1, device=torch.device("cpu"))
    assert absorption_indices[0] == -1

    # miss in x
    ray = Ray(
        position=Vector(1.5, -0.5, 0.5),
        velocity=Vector(0, 1, 0),
    )
    absorption_indices, _ = raytrace_event(all_elements=[element], all_rays=[ray], max_bounces=1, device=torch.device("cpu"))
    assert absorption_indices[0] == -1

    # miss in z
    ray = Ray(
        position=Vector(0.5, -0.5, 1.5),
        velocity=Vector(0, 1, 0),
    )
    absorption_indices, _ = raytrace_event(all_elements=[element], all_rays=[ray], max_bounces=1, device=torch.device("cpu"))
    assert absorption_indices[0] == -1


def test_z_rect_hit():
    element = RectElement(
        face=ZRectFace(x_min=0, x_max=1, y_min=0, y_max=1, z=0),
        reflectivity=0,
    )
    ray = Ray(
        position=Vector(0.5, 0.5, -0.5),
        velocity=Vector(0, 0, 1),
    )
    absorption_indices, absorption_times = raytrace_event(all_elements=[element], all_rays=[ray], max_bounces=1, device=torch.device("cpu"))
    assert absorption_indices[0] == 0
    assert absorption_times[0] == 0.5


def test_z_rect_no_hit():
    # wrong direction
    element = RectElement(
        face=ZRectFace(x_min=0, x_max=1, y_min=0, y_max=1, z=0),
        reflectivity=0,
    )
    ray = Ray(
        position=Vector(0.5, 0.5, 0.5),
        velocity=Vector(0, 0, 1),
    )
    absorption_indices, _ = raytrace_event(all_elements=[element], all_rays=[ray], max_bounces=1, device=torch.device("cpu"))
    assert absorption_indices[0] == -1

    # miss in x
    ray = Ray(
        position=Vector(1.5, 0.5, 0.5),
        velocity=Vector(0, 0, 1),
    )
    absorption_indices, _ = raytrace_event(all_elements=[element], all_rays=[ray], max_bounces=1, device=torch.device("cpu"))
    assert absorption_indices[0] == -1

    # miss in y
    ray = Ray(
        position=Vector(0.5, 1.5, 0.5),
        velocity=Vector(0, 0, 1),
    )
    absorption_indices, _ = raytrace_event(all_elements=[element], all_rays=[ray], max_bounces=1, device=torch.device("cpu"))
    assert absorption_indices[0] == -1


def test_inside_box_all_absorbed():
    all_elements = make_box_elements(
        x_min=-1, x_max=1,
        y_min=-1, y_max=1,
        z_min=-1, z_max=1,
        reflectivity=0,
    )
    all_rays = [
        Ray(
            position=Vector(random()-0.5, random()-0.5, random()-0.5),
            velocity=Vector(random()-0.5, random()-0.5, random()-0.5),
        )
        for _ in range(10)
    ]
    absorption_indices, absorption_times = raytrace_event(all_elements, all_rays, max_bounces=1, device=torch.device("cpu"))
    assert torch.all(absorption_indices >= 0)
    assert torch.all(absorption_times >= 0)


def test_sipms_absorb_all():
    scintillator_elements = make_box_elements(
        x_min=-1, x_max=1,
        y_min=-1, y_max=1,
        z_min=-1, z_max=1,
        reflectivity=1,
    )
    half_sipm_size = Vector(0.1, 0.1, 0.1)
    sipm_centers = [
        Vector(random()*1.8-0.9, random()*1.8-0.9, random()*1.8-0.9)
        for _ in range(10)
    ]
    sipm_elements = [
        make_box_elements(
            x_min=sipm_center.x-half_sipm_size.x,
            x_max=sipm_center.x+half_sipm_size.x,
            y_min=sipm_center.y-half_sipm_size.y,
            y_max=sipm_center.y+half_sipm_size.y,
            z_min=sipm_center.z-half_sipm_size.z,
            z_max=sipm_center.z+half_sipm_size.z,
            reflectivity=0,
        )
        for sipm_center in sipm_centers
    ]
    all_elements = scintillator_elements + [element for sipm_i_elements in sipm_elements for element in sipm_i_elements]
    all_rays = [
        Ray(
            position=Vector(random()-0.5, random()-0.5, random()-0.5),
            velocity=Vector(random()-0.5, random()-0.5, random()-0.5),
        )
        for _ in range(10)
    ]
    absorption_indices, absorption_times = raytrace_event(all_elements, all_rays, max_bounces=sys.maxsize, device=torch.device("cpu"))
    assert torch.all(absorption_indices >= 6)
    assert torch.all(absorption_times >= 0)
