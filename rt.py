import math
import sys
from rtutil import random_double

class Vec3:
    def __init__(self, e0=0, e1=0, e2=0):
        self.e = [e0, e1, e2]

    def x(self):
        return self.e[0]

    def y(self):
        return self.e[1]

    def z(self):
        return self.e[2]        

    def __neg__(self):
        x, y, z = self.e
        return Vec3(-x, -y, -z)

    def __getitem__(self, i):
        return self.e[i]

    def __add__(self, v):
        e0, e1, e2 = self.e
        f0, f1, f2 = v
        return Vec3(e0 + f0, e1 + f1, e2 + f2)

    def __sub__(self, v):
        e0, e1, e2 = self.e
        f0, f1, f2 = v
        return Vec3(e0 - f0, e1 - f1, e2 - f2)

    def __mul__(self, t):
        e0, e1, e2 = self.e
        if type(t) == int or type(t) == float:
            return Vec3(e0 * t, e1 * t, e2 * t)
        f0, f1, f2 = t.e
        return Vec3(e0 * f0, e1 * f1, e2 * f2)

    def __div__(self, t):
        return self * (1.0 / t)

    def div(self, t):
        return self * (1.0 / t)

    def __eq__(self, v):
        e0, e1, e2 = self.e
        f0, f1, f2 = v
        return e0 == f0 and e1 == f1 and e2 == f2

    def __str__(self):
        e0, e1, e2 = self.e
        return f"[{e0}, {e1}, {e2}]"

    def length(self):
        lsq = self.length_squared()
        return math.sqrt(lsq)

    def length_squared(self):
        e0, e1, e2 = self.e
        return (e0*e0) + (e1*e1) + (e2*e2)

    def dot(self, v):
        e0, e1, e2 = self.e
        f0, f1, f2 = v
        return (e0 * f0) + (e1 * f1) + (e2 * f2)

    def cross(self, v):
        e0, e1, e2 = self.e
        f0, f1, f2 = v

        return Vec3(
            (e1 * f2) - (e2 * f1),
            (e2 * f0) - (e0 * f2),
            (e0 * f1) - (e1 * f0)
        )

    def unit_vector(self):
        return self.__div__(self.length())

    def write(self):
        print(" ".join(str(int(255.999 * c)) for c in self.e))
    
    def near_zero(self):
        s = 0.000001
        return (abs(self.e[0]) < s) and (abs(self.e[1]) < s) and (abs(self.e[2]) < s)

    def update(self, v):
        self.e = [e for e in v.e]

    __rmul__ = __mul__
    __radd__ = __add__

class Point3(Vec3):
    pass

class Color(Vec3):
    pass


class Ray():
    def __init__(self, origin=None, direction=None):
        self.origin = origin if origin else Point3()
        self.direction = direction if direction else Vec3()

    def at(self, t):
        return self.origin + (t * self.direction)

    def update(self, r):
        self.origin = r.origin
        self.direction = r.direction

class HitRecord:
    def __init__(self, point=None, normal=None, material=None, t=None, front_face=None):
        self.point = point
        self.normal = normal
        self.material = material
        self.t = t
        self.front_face = front_face

    def update(self, new_rec):
        self.point = new_rec.point
        self.normal = new_rec.normal
        self.material = new_rec.material
        self.t = new_rec.t
        self.front_face = new_rec.front_face
        
    def set_face_normal(self, r, outward_normal):
        self.front_face = r.direction.dot(outward_normal) < 0
        self.normal = outward_normal if self.front_face  else -outward_normal

class Sphere:
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def hit(self, r, t_min, t_max, rec):
        oc = r.origin - self.center
        a = r.direction.length_squared()
        half_b = oc.dot(r.direction)        
        c = oc.length_squared() - (self.radius ** 2)
        
        discriminant = (half_b * half_b) - (a * c)
        if discriminant < 0:
            return False
        sqrtd = math.sqrt(discriminant)

        root = (-half_b - sqrtd) / a
        if (root < t_min or t_max < root):
            root = (-half_b + sqrtd) / a
            if (root < t_min or t_max < root):
                return False
        
        rec.t = root
        rec.point = r.at(rec.t)
        outward_normal = (rec.point - self.center).div(self.radius)
        rec.set_face_normal(r, outward_normal)
        rec.material = self.material

        return True

class HittableList:
        def __init__(self, objects=None):
            if objects and len(objects) > 0:
                self.objects = [o for o in objects]
            else:
                self.objects = []

        def add(self, obj):
            self.objects.append(obj)

        def clear(self):
            self.objects.clear()

        def hit(self, r, t_min, t_max, rec):
            hit_something = False
            closest_obj_t = t_max

            for obj in self.objects:
                temp_rec = HitRecord()
                if obj.hit(r, t_min, closest_obj_t, temp_rec):
                    hit_something = True
                    closest_obj_t = temp_rec.t
                    rec.update(temp_rec)

            return hit_something

class Camera:
    def __init__(self, lookfrom, lookat, vup, vfov, aspect_ratio, aperture, focus_distance):
        theta = math.radians(vfov)
        h = math.tan(theta / 2)
        viewport_height = 2.0 * h
        viewport_width = aspect_ratio * viewport_height

        self.w = (lookfrom - lookat).unit_vector()
        self.u = vup.cross(self.w).unit_vector()
        self.v = self.w.cross(self.u)

        focal_length = 1.0

        self.origin = lookfrom
        self.horizontal = focus_distance * viewport_width * self.u
        self.vertical = focus_distance * viewport_height * self.v        
        self.lower_left_corner = self.origin - self.horizontal.div(2) - self.vertical.div(2) - (focus_distance * self.w)

        self.lens_radius = aperture / 2

    def get_ray(self, s, t):
        rd = self.lens_radius * random_in_unit_disk()
        offset = (self.u * rd.x()) + (self.v * rd.y())

        return Ray(
            self.origin + offset,
            self.lower_left_corner + (s * self.horizontal) + (t * self.vertical) - self.origin - offset
        )

class Material:
    def scatter(self, r_in, rec, attenuation, scattered):
        return False

class Lambertian(Material):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, r_in, rec, attenuation, scattered):
        scatter_direction = rec.normal + random_unit_vector()

        if scatter_direction.near_zero():
            scatter_direction = rec.normal;

        scattered.update(Ray(rec.point, scatter_direction))
        attenuation.update(self.albedo)
        return True

def random_color(min=0.0, max=1.0):
    return Color(random_double(min, max), random_double(min, max), random_double(min, max))

def random_vec3(min=0.0, max=1.0):
    return Vec3(random_double(min, max), random_double(min, max), random_double(min, max))

def random_vec3_in_unit_sphere():
    while True:
        p = random_vec3(-1, 1)
        if p.length_squared() >= 1:
            continue
        return p

def random_unit_vector():
    return random_vec3_in_unit_sphere().unit_vector()

def random_in_hemisphere(normal):
    in_unit_sphere = random_vec3_in_unit_sphere()
    if (in_unit_sphere.dot(normal) > 0.0):
        return in_unit_sphere
    else:
        return -in_unit_sphere

def reflect(v, n):
    return v - (2 * (v.dot(n) * n))

class Metal(Material):
    def __init__(self, albedo, fuzz):
        self.albedo = albedo
        self.fuzz = fuzz

    def scatter(self, r_in, rec, attenuation, scattered):
        reflected = reflect(r_in.direction.unit_vector(), rec.normal)
        scattered.update(Ray(rec.point, reflected + (self.fuzz * random_vec3_in_unit_sphere())))
        attenuation.update(self.albedo)
        return scattered.direction.dot(rec.normal) > 0

def refract(uv, n, etai_over_etat):
    cos_theta     = min((-uv).dot(n), 1.0)
    r_out_perp = etai_over_etat * (uv + cos_theta * n)
    r_out_parallel = -math.sqrt(abs(1.0 - r_out_perp.length_squared())) * n
    return r_out_perp + r_out_parallel

def reflectance(cosine, ref_idx):
    r0 = (1-ref_idx) / (1+ref_idx);
    r0 = r0*r0
    return r0 + (1-r0)*math.pow((1 - cosine),5)

class Dielectric(Material):
    def __init__(self, ir):
        self.ir = ir

    def refraction_ratio(self, rec):
        if rec.front_face:
            return 1.0 / self.ir
        else:
            return self.ir

    def scatter(self, r_in, rec, attenuation, scattered):
        attenuation.update(Color(1.0, 1.0, 1.0))
        rr = self.refraction_ratio(rec)

        unit_direction = r_in.direction.unit_vector()

        cos_theta = min((-unit_direction).dot(rec.normal), 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta**2)

        cannot_refract = rr * sin_theta > 1.0
        maybe_dont_refract = reflectance(cos_theta, rr) > random_double()

        direction = reflect(unit_direction, rec.normal) if cannot_refract or maybe_dont_refract else refract(unit_direction, rec.normal, rr)

        scattered.update(Ray(rec.point, direction))
        return True


# vec3 random_in_unit_disk() {
#     while (true) {
#         auto p = vec3(random_double(-1,1), random_double(-1,1), 0);
#         if (p.length_squared() >= 1) continue;
#         return p;
#     }
# }

def random_in_unit_disk():
    while True:
        p = Vec3(random_double(-1, 1), random_double(-1, 1), 0)
        if p.length_squared() < 1:
            return p