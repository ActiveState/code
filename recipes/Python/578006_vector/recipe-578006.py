from math import *
from functools import wraps

################################################################################

def autocast(method): # Optional method decorator
    @wraps(method)
    def wrapper(self, obj):
        try:
            return method(self, self.__class__(*obj))
        except TypeError:
            return method(self, obj)
    return wrapper

################################################################################

def Polar2(magnitude, degrees):
    x = magnitude * sin(radians(degrees))
    y = magnitude * cos(radians(degrees))
    return Vector2(x, y)

################################################################################

class Vector2:

    __slots__ = 'x', 'y'

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Vector2({!r}, {!r})'.format(self.x, self.y)

    def polar_repr(self):
        x, y = self.x, self.y
        magnitude = hypot(x, y)
        angle = degrees(atan2(x, y)) % 360
        return 'Polar2({!r}, {!r})'.format(magnitude, angle)

    # Rich Comparison Methods

    def __lt__(self, obj):
        if isinstance(obj, Vector2):
            x1, y1, x2, y2 = self.x, self.y, obj.x, obj.y
            return x1 * x1 + y1 * y1 < x2 * x2 + y2 * y2
        return hypot(self.x, self.y) < obj

    def __le__(self, obj):
        if isinstance(obj, Vector2):
            x1, y1, x2, y2 = self.x, self.y, obj.x, obj.y
            return x1 * x1 + y1 * y1 <= x2 * x2 + y2 * y2
        return hypot(self.x, self.y) <= obj

    def __eq__(self, obj):
        if isinstance(obj, Vector2):
            return self.x == obj.x and self.y == obj.y
        return hypot(self.x, self.y) == obj

    def __ne__(self, obj):
        if isinstance(obj, Vector2):
            return self.x != obj.x or self.y != obj.y
        return hypot(self.x, self.y) != obj

    def __gt__(self, obj):
        if isinstance(obj, Vector2):
            x1, y1, x2, y2 = self.x, self.y, obj.x, obj.y
            return x1 * x1 + y1 * y1 > x2 * x2 + y2 * y2
        return hypot(self.x, self.y) > obj

    def __ge__(self, obj):
        if isinstance(obj, Vector2):
            x1, y1, x2, y2 = self.x, self.y, obj.x, obj.y
            return x1 * x1 + y1 * y1 >= x2 * x2 + y2 * y2
        return hypot(self.x, self.y) >= obj

    # Boolean Operation

    def __bool__(self):
        return self.x != 0 or self.y != 0

    # Container Methods

    def __len__(self):
        return 2

    def __getitem__(self, index):
        return (self.x, self.y)[index]

    def __setitem__(self, index, value):
        temp = [self.x, self.y]
        temp[index] = value
        self.x, self.y = temp

    def __iter__(self):
        yield self.x
        yield self.y

    def __reversed__(self):
        yield self.y
        yield self.x

    def __contains__(self, obj):
        return obj in (self.x, self.y)

    # Binary Arithmetic Operations

    def __add__(self, obj):
        if isinstance(obj, Vector2):
            return Vector2(self.x + obj.x, self.y + obj.y)
        return Vector2(self.x + obj, self.y + obj)

    def __sub__(self, obj):
        if isinstance(obj, Vector2):
            return Vector2(self.x - obj.x, self.y - obj.y)
        return Vector2(self.x - obj, self.y - obj)

    def __mul__(self, obj):
        if isinstance(obj, Vector2):
            return Vector2(self.x * obj.x, self.y * obj.y)
        return Vector2(self.x * obj, self.y * obj)

    def __truediv__(self, obj):
        if isinstance(obj, Vector2):
            return Vector2(self.x / obj.x, self.y / obj.y)
        return Vector2(self.x / obj, self.y / obj)

    def __floordiv__(self, obj):
        if isinstance(obj, Vector2):
            return Vector2(self.x // obj.x, self.y // obj.y)
        return Vector2(self.x // obj, self.y // obj)

    def __mod__(self, obj):
        if isinstance(obj, Vector2):
            return Vector2(self.x % obj.x, self.y % obj.y)
        return Vector2(self.x % obj, self.y % obj)

    def __divmod__(self, obj):
        if isinstance(obj, Vector2):
            return (Vector2(self.x // obj.x, self.y // obj.y),
                    Vector2(self.x % obj.x, self.y % obj.y))
        return (Vector2(self.x // obj, self.y // obj),
                Vector2(self.x % obj, self.y % obj))

    def __pow__(self, obj):
        if isinstance(obj, Vector2):
            return Vector2(self.x ** obj.x, self.y ** obj.y)
        return Vector2(self.x ** obj, self.y ** obj)

    def __lshift__(self, obj):
        if isinstance(obj, Vector2):
            return Vector2(self.x << obj.x, self.y << obj.y)
        return Vector2(self.x << obj, self.y << obj)

    def __rshift__(self, obj):
        if isinstance(obj, Vector2):
            return Vector2(self.x >> obj.x, self.y >> obj.y)
        return Vector2(self.x >> obj, self.y >> obj)

    def __and__(self, obj):
        if isinstance(obj, Vector2):
            return Vector2(self.x & obj.x, self.y & obj.y)
        return Vector2(self.x & obj, self.y & obj)

    def __xor__(self, obj):
        if isinstance(obj, Vector2):
            return Vector2(self.x ^ obj.x, self.y ^ obj.y)
        return Vector2(self.x ^ obj, self.y ^ obj)

    def __or__(self, obj):
        if isinstance(obj, Vector2):
            return Vector2(self.x | obj.x, self.y | obj.y)
        return Vector2(self.x | obj, self.y | obj)

    # Binary Arithmetic Operations (with reflected operands)

    def __radd__(self, obj):
        return Vector2(obj + self.x, obj + self.y)

    def __rsub__(self, obj):
        return Vector2(obj - self.x, obj - self.y)

    def __rmul__(self, obj):
        return Vector2(obj * self.x, obj * self.y)

    def __rtruediv__(self, obj):
        return Vector2(obj / self.x, obj / self.y)

    def __rfloordiv__(self, obj):
        return Vector2(obj // self.x, obj // self.y)

    def __rmod__(self, obj):
        return Vector2(obj % self.x, obj % self.y)

    def __rdivmod__(self, obj):
        return (Vector2(obj // self.x, obj // self.y),
                Vector2(obj % self.x, obj % self.y))

    def __rpow__(self, obj):
        return Vector2(obj ** self.x, obj ** self.y)

    def __rlshift__(self, obj):
        return Vector2(obj << self.x, obj << self.y)

    def __rrshift__(self, obj):
        return Vector2(obj >> self.x, obj >> self.y)

    def __rand__(self, obj):
        return Vector2(obj & self.x, obj & self.y)

    def __rxor__(self, obj):
        return Vector2(obj ^ self.x, obj ^ self.y)

    def __ror__(self, obj):
        return Vector2(obj | self.x, obj | self.y)

    # Augmented Arithmetic Assignments

    def __iadd__(self, obj):
        if isinstance(obj, Vector2):
            self.x += obj.x
            self.y += obj.y
        else:
            self.x += obj
            self.y += obj
        return self

    def __isub__(self, obj):
        if isinstance(obj, Vector2):
            self.x -= obj.x
            self.y -= obj.y
        else:
            self.x -= obj
            self.y -= obj
        return self

    def __imul__(self, obj):
        if isinstance(obj, Vector2):
            self.x *= obj.x
            self.y *= obj.y
        else:
            self.x *= obj
            self.y *= obj
        return self

    def __itruediv__(self, obj):
        if isinstance(obj, Vector2):
            self.x /= obj.x
            self.y /= obj.y
        else:
            self.x /= obj
            self.y /= obj
        return self

    def __ifloordiv__(self, obj):
        if isinstance(obj, Vector2):
            self.x //= obj.x
            self.y //= obj.y
        else:
            self.x //= obj
            self.y //= obj
        return self

    def __imod__(self, obj):
        if isinstance(obj, Vector2):
            self.x %= obj.x
            self.y %= obj.y
        else:
            self.x %= obj
            self.y %= obj
        return self

    def __ipow__(self, obj):
        if isinstance(obj, Vector2):
            self.x **= obj.x
            self.y **= obj.y
        else:
            self.x **= obj
            self.y **= obj
        return self

    def __ilshift__(self, obj):
        if isinstance(obj, Vector2):
            self.x <<= obj.x
            self.y <<= obj.y
        else:
            self.x <<= obj
            self.y <<= obj
        return self

    def __irshift__(self, obj):
        if isinstance(obj, Vector2):
            self.x >>= obj.x
            self.y >>= obj.y
        else:
            self.x >>= obj
            self.y >>= obj
        return self

    def __iand__(self, obj):
        if isinstance(obj, Vector2):
            self.x &= obj.x
            self.y &= obj.y
        else:
            self.x &= obj
            self.y &= obj
        return self

    def __ixor__(self, obj):
        if isinstance(obj, Vector2):
            self.x ^= obj.x
            self.y ^= obj.y
        else:
            self.x ^= obj
            self.y ^= obj
        return self

    def __ior__(self, obj):
        if isinstance(obj, Vector2):
            self.x |= obj.x
            self.y |= obj.y
        else:
            self.x |= obj
            self.y |= obj
        return self

    # Unary Arithmetic Operations

    def __pos__(self):
        return Vector2(+self.x, +self.y)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __invert__(self):
        return Vector2(~self.x, ~self.y)

    def __abs__(self):
        return Vector2(abs(self.x), abs(self.y))

    # Virtual "magnitude" Attribute

    def __fg_ma(self):
        return hypot(self.x, self.y)

    def __fs_ma(self, value):
        x, y = self.x, self.y
        temp = value / hypot(x, y)
        self.x, self.y = x * temp, y * temp

    magnitude = property(__fg_ma, __fs_ma, doc='Virtual "magnitude" Attribute')

    # Virtual "direction" Attribute

    def __fg_di(self):
        return atan2(self.y, self.x)

    def __fs_di(self, value):
        temp = hypot(self.x, self.y)
        self.x, self.y = cos(value) * temp, sin(value) * temp

    direction = property(__fg_di, __fs_di, doc='Virtual "direction" Attribute')

    # Virtual "degrees" Attribute

    def __fg_de(self):
        return degrees(atan2(self.x, self.y)) % 360

    def __fs_de(self, value):
        value, temp = radians(value), hypot(self.x, self.y)
        self.x, self.y = sin(value) * temp, cos(value) * temp

    degrees = property(__fg_de, __fs_de, doc='Virtual "degrees" Attribute')

    # Virtual "xy" Attribute

    def __fg_xy(self):
        return self.x, self.y

    def __fs_xy(self, value):
        self.x, self.y = value

    xy = property(__fg_xy, __fs_xy, doc='Virtual "xy" Attribute')

    # Virtual "yx" Attribute

    def __fg_yx(self):
        return self.y, self.x

    def __fs_yx(self, value):
        self.y, self.x = value

    yx = property(__fg_yx, __fs_yx, doc='Virtual "yx" Attribute')

    # Unit Vector Operations

    def unit_vector(self):
        x, y = self.x, self.y
        temp = hypot(x, y)
        return Vector2(x / temp, y / temp)

    def normalize(self):
        x, y = self.x, self.y
        temp = hypot(x, y)
        self.x, self.y = x / temp, y / temp
        return self

    # Vector Multiplication Operations

    def dot_product(self, vec):
        return self.x * vec.x + self.y * vec.y

    def cross_product(self, vec):
        return self.x * vec.y - self.y * vec.x

    # Geometric And Physical Reflections

    def reflect(self, vec):
        x1, y1, x2, y2 = self.x, self.y, vec.x, vec.y
        temp = 2 * (x1 * x2 + y1 * y2) / (x2 * x2 + y2 * y2)
        return Vector2(x2 * temp - x1, y2 * temp - y1)

    def bounce(self, vec):
        x1, y1, x2, y2 = self.x, self.y, +vec.y, -vec.x
        temp = 2 * (x1 * x2 + y1 * y2) / (x2 * x2 + y2 * y2)
        return Vector2(x2 * temp - x1, y2 * temp - y1)

    # Standard Vector Operations

    def project(self, vec):
        x, y = vec.x, vec.y
        temp = (self.x * x + self.y * y) / (x * x + y * y)
        return Vector2(x * temp, y * temp)

    def rotate(self, vec):
        x1, y1, x2, y2 = self.x, self.y, vec.x, vec.y
        return Vector2(x1 * x2 + y1 * y2, y1 * x2 - x1 * y2)

    def interpolate(self, vec, bias):
        a = 1 - bias
        return Vector2(self.x * a + vec.x * bias, self.y * a + vec.y * bias)

    # Other Useful Methods

    def near(self, vec, dist):
        x, y = self.x - vec.x, self.y - vec.y
        return x * x + y * y <= dist * dist

    def perpendicular(self):
        return Vector2(+self.y, -self.x)

    def subset(self, vec1, vec2):
        x1, x2 = vec1.x, vec2.x
        if x1 <= x2:
            if x1 <= self.x <= x2:
                y1, y2 = vec1.y, vec2.y
                if y1 <= y2:
                    return y1 <= self.y <= y2
                return y2 <= self.y <= y1
        else:
            if x2 <= self.x <= x1:
                y1, y2 = vec1.y, vec2.y
                if y1 <= y2:
                    return y1 <= self.y <= y2
                return y2 <= self.y <= y1
        return False

    def distance(self, vec):
        return hypot(self.x - vec.x, self.y - vec.y)

    def limit(self, dist):
        x, y = self.x, self.y
        magnitude = hypot(x, y)
        if magnitude > dist:
            temp = dist / magnitude
            self.x, self.y = x * temp, y * temp
        return self

    def direction_between(self, vec):
        return atan2(self.y, self.x) - atan2(vec.y, vec.x)

    def degrees_between(self, vec):
        diff = degrees(atan2(self.y, self.x) - atan2(vec.y, vec.x)) % 360
        return 360 - diff if diff > 180 else diff

    # Synonymous Definitions

    copy = __pos__

    inverse = __neg__

    unit = unit_vector

    dot = dot_product

    cross = cross_product

    lerp = interpolate

    perp = perpendicular

    dist = distance

    dir_diff = direction_between

    deg_diff = degrees_between

################################################################################

import recipe576904; recipe576904.bind_all(globals())
