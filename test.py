from rt import Vec3, Color, Point3, Ray
import sys

def ray_color(r):
    t = r.hit_sphere(Point3(0.0, 0.0, -1.0), 0.5)

    if (t > 0.0):
        n = (r.at(t) - Vec3(0, 0, -1.0)).unit_vector()
        return 0.5 * Color(n.x() + 1.0, n.y() + 1.0, n.z() + 1.0)

    unit_direction = r.direction.unit_vector()
    t = 0.5 * (unit_direction.y() + 1.0)
    return (1.0 - t) * Color(1.0, 1.0, 1.0) + (t * Color(0.5, 0.7, 1.0))

# Image
aspect_ratio = 16.0 / 9.0
image_width = 400
image_height = image_width / aspect_ratio

# Camera
viewport_height = 2.0
viewport_width = aspect_ratio * viewport_height
focal_length = 1.0
origin = Point3(0.0, 0.0, 0.0)
horizontal = Vec3(viewport_width, 0,               0)
vertical   = Vec3(0,              viewport_height, 0)
lower_left_corner = origin - horizontal.div(2) - vertical.div(2) - Vec3(0, 0, focal_length)

print(origin, file=sys.stderr)
print(lower_left_corner, file=sys.stderr)

print("P3")
print(int(image_width), int(image_height))
print(255)

for y in range(int(image_height), 0, -1):
    for x in range(int(image_width)):
        u = x / (image_width - 1)
        v = y / (image_height - 1)
        r = Ray(origin, lower_left_corner + (u*horizontal) + (v*vertical) - origin)
        c = ray_color(r)
        c.write()