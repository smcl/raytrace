from rt import Vec3, Color, Point3, Ray, HitRecord, Sphere, HittableList, Camera, random_vec3, random_vec3_in_unit_sphere, random_unit_vector, random_in_hemisphere, Lambertian, Material, Metal, Dielectric, random_color
from rtutil import compute_color, random_double
import sys
import math
from multiprocessing import Pool
from itertools import chain

def ray_color(r, world, depth):
    if depth <= 0:
        return Color(0, 0, 0)

    rec = HitRecord()
    if world.hit(r, 0.00001, math.inf, rec):
        scattered = Ray(0, 0)
        attenuation = Color()

        if rec.material.scatter(r, rec, attenuation, scattered):
            return attenuation * ray_color(scattered, world, depth-1)

        return Color(0, 0, 0)

    unit_direction = r.direction.unit_vector()
    t = 0.5 * (unit_direction.y() + 1.0)
    return (1.0 - t) * Color(1.0, 1.0, 1.0) + (t * Color(0.5, 0.7, 1.0))

def compute_rows(compute_args):
    world, camera, start, lines_per_process = compute_args
    result = []
    for y in range(start, start-lines_per_process, -1):
        for x in range(int(image_width)):
            pixel_color = Color()
            for _ in range(samples_per_pixel):
                u = (random_double() + x) / (image_width - 1)
                v = (random_double() + y) / (image_height - 1)
                r = camera.get_ray(u, v)
                pixel_color += ray_color(r, world, max_depth)
            c = compute_color(pixel_color, samples_per_pixel)
            result.append(c)
    return result


def simple_world():
    world = HittableList()

    material_ground = Lambertian(Color(0.8, 0.8, 0.0))
    material_red = Lambertian(Color(0.7, 0.3, 0.3))
    material_green = Lambertian(Color(0.3, 0.7, 0.3))
    material_shiny = Metal(Color(0.8, 0.8, 0.8), 0.0)
    material_glass = Dielectric(1.5)
    material_right = Metal(Color(0.8, 0.6, 0.2), 0.5)

    world.add(Sphere(Point3( 0.0, -100.5, -1.0), 100.0, material_ground))
    world.add(Sphere(Point3( 0.0,    0.0, -1.0),   0.5, material_red))
    world.add(Sphere(Point3(-1.0,    0.0, -1.0),  -0.5, material_glass))
    world.add(Sphere(Point3( 1.0,    0.0, -1.0),   0.5, material_shiny))
    world.add(Sphere(Point3( 0.0,    0.0,  0.0),   0.5, material_shiny))
    world.add(Sphere(Point3( 0.0,     0.0, -4.0),  0.5, material_green))

    return world


def random_world():
    world = HittableList()

    ground_material = Lambertian(Color(0.5, 0.5, 0.5))
    world.add(Sphere(Point3(0, -1000, 0), 1000, ground_material))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random_double()
            center = Point3(
                a + 0.9 * random_double(),
                0.2,
                b + 0.9 * random_double()
            )

            if (center - Point3(4, 0.2, 0)).length() > 0.9:
                if choose_mat < 0.8:
                    albedo = random_color() * random_color()
                    sphere_material = Lambertian(albedo)
                    world.add(Sphere(center, 0.2, sphere_material))
                elif choose_mat < 0.95:
                    albedo = random_color(0.5, 1)
                    fuzz = random_double(0, 0.5)
                    sphere_material = Metal(albedo, fuzz)
                    world.add(Sphere(center, 0.2, sphere_material))
                else:
                    sphere_material = Dielectric(1.5)
                    world.add(Sphere(center, 0.2, sphere_material))
    
    material1 = Dielectric(1.5)
    world.add(Sphere(Point3(0, 1, 0), 1.0, material1))

    material2 = Lambertian(Color(0.4, 0.2, 0.1))
    world.add(Sphere(Point3(-4, 1, 0), 1.0, material2))

    material3 = Metal(Color(0.7, 0.6, 0.5), 0.0)
    world.add(Sphere(Point3(4, 1, 0), 1.0, material3))

    return world
    
# Image
aspect_ratio = 3.0 / 2.0 #16.0 / 9.0
image_width = 1600
image_height = int(image_width / aspect_ratio)
samples_per_pixel = 100
max_depth = 50

# Camera
# lookfrom = Point3(3, 3, 2)
# lookat = Point3(0, 0, -1)
# vup = Vec3(0, 1, 0)
# aperture = 0.1
# dist_to_focus = (lookfrom-lookat).length()
lookfrom = Point3(13, 2, 3)
lookat = Point3(0, 0, 0)
vup = Vec3(0, 1, 0)
aperture = 0.1
dist_to_focus = 10

camera = Camera(
    lookfrom,
    lookat,
    vup,
    30,
    aspect_ratio,
    aperture,
    dist_to_focus
)

# World
world = random_world() 
#world = simple_world()

num_processes = 10

if __name__ == '__main__':
    print("P3")
    print(int(image_width), int(image_height))
    print(255)    
    lines_per_process = image_height // num_processes
    chunks = list(reversed([ (world, camera, n * lines_per_process, lines_per_process) for n in range(0, 1 + num_processes)]))
    with Pool(num_processes) as p:
        result_chunks = p.map(compute_rows, chunks)
        rows = chain.from_iterable(result_chunks)
        print("\n".join(rows))