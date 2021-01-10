from rt import Vec3, Color, Point3, Ray
import sys

def ray_color(r):
    if r.hit_sphere(Point3(0, 0, -0.75), 0.25):
        return Color(0, 1, 0)

    if r.hit_sphere(Point3(0, 0.1, -1), 0.5):
        return Color(1, 0, 0)     

    unit_direction = r.direction.unit_vector()
    t = 0.5 * (unit_direction.y() + 1.0)
    return (1.0 - t) * Color(1.0, 1.0, 1.0) + (t * Color(0.5, 0.7, 1.0))

# Image
aspect_ratio = 2.0 # 16.0 / 9.0
image_width = 600
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
        #r = Ray(origin, lower_left_corner + (u*horizontal) + (v*vertical) - origin)
        r = Ray(origin, lower_left_corner + (u*horizontal) + (v*vertical))
        c = ray_color(r)

        c.write()