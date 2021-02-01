import random
import math

def random_double(min=0.0, max=1.0):
    return min + (max - min) * random.random()

def clamp(x, min, max):
    if x < min:
        return min

    if x > max:
         return max

    return x

def compute_color(color, samples_per_pixel):
    r = color.x()
    g = color.y()
    b = color.z()

    scale = 1.0 / samples_per_pixel
    r = math.sqrt(scale * r)
    g = math.sqrt(scale * g)
    b = math.sqrt(scale * b)

    clamped_r = int(256 * clamp(r, 0.0, 0.999))
    clamped_g = int(256 * clamp(g, 0.0, 0.999))
    clamped_b = int(256 * clamp(b, 0.0, 0.999))

    return f"{clamped_r} {clamped_g} {clamped_b}"
