from rt import Vec3, Color, Point3, Ray, HitRecord, Sphere, HittableList, Camera
from rtutil import write_color, random_double, random_vec3, random_vec3_in_unit_sphere
import sys
import math

def ray_color(r, world, depth):
    if depth <= 0:
        return Color(0, 0, 0)

    rec = HitRecord()
    if world.hit(r, 0, math.inf, rec):
        target = rec.point + rec.normal + random_vec3_in_unit_sphere()
        return 0.5 * ray_color(Ray(rec.point, target - rec.point), world, depth -1)

    unit_direction = r.direction.unit_vector()
    t = 0.5 * (unit_direction.y() + 1.0)
    return (1.0 - t) * Color(1.0, 1.0, 1.0) + (t * Color(0.5, 0.7, 1.0))

# Image
aspect_ratio = 16.0 / 9.0
image_width = 400
image_height = image_width / aspect_ratio
samples_per_pixel = 100
max_depth = 50

# Camera
camera = Camera()

# World
world = HittableList()
world.add(Sphere(Point3(0, 0, -1), 0.5))
world.add(Sphere(Point3(0, -100.5, -1), 100))

# print(origin, file=sys.stderr)
# print(lower_left_corner, file=sys.stderr)

print("P3")
print(int(image_width), int(image_height))
print(255)

for y in range(int(image_height), 0, -1):
    for x in range(int(image_width)):
        pixel_color = Color()
        for _ in range(samples_per_pixel):
            u = (random_double() + x) / (image_width - 1)
            v = (random_double() + y) / (image_height - 1)
            r = camera.get_ray(u, v)
            pixel_color += ray_color(r, world, max_depth)
        write_color(pixel_color, samples_per_pixel)