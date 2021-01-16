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

    def hit_sphere(self, center, radius):
        oc = self.origin - center
        a = self.direction.dot(self.direction)
        b = 2.0 * oc.dot(self.direction)
        c = oc.dot(oc) - (radius ** 2)
        discriminant = (b*b) - (4*a*c)

        if discriminant < 0:
            return -1.0
        
        return ((-b) - math.sqrt(discriminant)) / (2.0 * a)

    def at(self, t):
        return self.origin + (t * self.direction)
