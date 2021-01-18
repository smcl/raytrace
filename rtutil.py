from rt import Vec3
import random

def random_double(min=0.0, max=1.0):
    return min + (max - min) * random.random()

def clamp(x, min, max):
    if x < min:
        return min

    if x > max:
         return max

    return x

def write_color(color, samples_per_pixel):
    r = color.x()
    g = color.y()
    b = color.z()

    scale = 1.0 / samples_per_pixel
    r *= scale
    g *= scale
    b *= scale

    clamped_r = int(256 * clamp(r, 0.0, 0.999))
    clamped_g = int(256 * clamp(g, 0.0, 0.999))
    clamped_b = int(256 * clamp(b, 0.0, 0.999))

    print(f"{clamped_r} {clamped_g} {clamped_b}")

def random_vec3(min=0.0, max=1.0):
    return Vec3(random_double(min, max), random_double(min, max), random_double(min, max))

def random_vec3_in_unit_sphere():
    while True:
        p = random_vec3(-1, 1)
        if p.length_squared() >= 1:
            continue
        return p