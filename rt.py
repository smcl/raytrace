import math

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
        return Vec3(x, y, z)

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
    
    __rmul__ = __mul__
    __radd__ = __add__

class Point3(Vec3):
    pass

class Color(Vec3):
    pass


class Ray():
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def at(self, t):
        return self.origin + (t * self.direction)

class HitRecord:
    def __init__(self, point=None, normal=None, t=None, front_face=None):
        self.point = point
        self.normal = normal
        self.t = t
        self.front_face = front_face

    def update(self, new_rec):
        self.point = new_rec.point
        self.normal = new_rec.normal
        self.t = new_rec.t
        self.front_face = new_rec.front_face
        
    def set_face_normal(self, r, outward_normal):
        self.front_face = r.direction.dot(outward_normal) < 0
        self.normal = outward_normal if self.front_face  else -outward_normal

class Sphere:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

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
    def __init__(self):
        aspect_ratio = 16.0 / 9.0
        viewport_height = 2.0
        viewport_width = aspect_ratio * viewport_height
        focal_length = 1.0

        self.origin = Point3(0.0, 0.0, 0.0)
        self.horizontal = Vec3(viewport_width, 0,               0)
        self.vertical   = Vec3(0,              viewport_height, 0)
        self.lower_left_corner = self.origin - self.horizontal.div(2) - self.vertical.div(2) - Vec3(0, 0, focal_length)

    def get_ray(self, u, v):
        return Ray(self.origin, self.lower_left_corner + (u * self.horizontal) + (v * self.vertical) - self.origin)
