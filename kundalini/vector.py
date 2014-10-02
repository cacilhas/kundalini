import math
from numbers import Number
from collections import namedtuple


class Vector(namedtuple('Vector', 'x y z w')):

    def __new__(cls, x:float=0., y:float=0., z:float=0., w:float=0.) -> namedtuple:
        return super(Vector, cls).__new__(cls, x, y, z, w)


    #---------------------------------------------------------------
    @property
    def magnitude(self) -> float:
        if not hasattr(self, '_maginitude'):
            mag = math.sqrt(pow(self.x, 2) + pow(self.y, 2))
            mag = math.sqrt(pow(mag, 2) + pow(self.z, 2))
            self._magnitude = math.sqrt(pow(mag, 2) + pow(self.w, 2))
        return self._magnitude


    #---------------------------------------------------------------
    @property
    def angles(self) -> tuple:
        if not hasattr(self, '_angles'):
            mag = math.sqrt(pow(self.x, 2) + pow(self.y, 2))
            sin = self.y / mag
            angles = [math.asin(sin)]

            mag = math.sqrt(pow(self.x, 2) + pow(self.z, 2))
            sin = self.z / mag
            angles.append(math.asin(sin))

            mag = math.sqrt(pow(self.x, 2) + pow(self.w, 2))
            sin = self.w / mag
            angles.append(math.asin(sin))

            self._angles = tuple(map(math.degrees, angles))
        return self._angles


    #---------------------------------------------------------------
    @classmethod
    def from_angles(cls, magnitude, *angles) -> namedtuple:
        angles += (0, 0, 0)
        angles = tuple(map(math.radians, angles[:3]))
        x = math.cos(angles[0])
        y = math.sin(angles[0])

        ax = math.cos(angles[1])
        z = math.sin(angles[1])
        y = y * ax / x
        x = ax

        ax = math.cos(angles[2])
        w = math.sin(angles[2])
        z = z * ax / x
        y = y * ax / x
        x = ax

        vector = cls(x, y, z, w)
        mag = vector.magnitude
        return vector * magnitude / mag


    #---------------------------------------------------------------
    def __abs__(self) -> namedtuple:
        return type(self)(
            x = abs(self.x),
            y = abs(self.y),
            z = abs(self.z),
            w = abs(self.w),
        )


    #---------------------------------------------------------------
    def __neg__(self) -> namedtuple:
        return type(self)(
            x = -self.x,
            y = -self.y,
            z = -self.z,
            w = -self.w,
        )


    #---------------------------------------------------------------
    def __pos__(self) -> namedtuple:
        return self


    #---------------------------------------------------------------
    def __add__(self, other:tuple) -> namedtuple:
        other += (0, 0, 0, 0)
        return type(self)(
            x = self.x + other[0],
            y = self.y + other[1],
            z = self.z + other[2],
            w = self.w + other[3],
        )

    __radd__ = __add__


    #---------------------------------------------------------------
    def __sub__(self, other:tuple) -> namedtuple:
        other += (0, 0, 0, 0)
        return type(self)(
            x = self.x - other[0],
            y = self.y - other[1],
            z = self.z - other[2],
            w = self.w - other[3],
        )

    def __rsub__(self, other:tuple) -> namedtuple:
        other += (0, 0, 0, 0)
        return type(self)(
            x = other[0] - self.x,
            y = other[1] - self.y,
            z = other[2] - self.z,
            w = other[3] - self.w,
        )


    #---------------------------------------------------------------
    def __mul__(self, other:Number) -> namedtuple:
        return type(self)(
            x = self.x * other,
            y = self.y * other,
            z = self.z * other,
            w = self.w * other,
        )

    __rmul__ = __mul__


    #---------------------------------------------------------------
    def __truediv__(self, other:Number) -> namedtuple:
        return type(self)(
            x = self.x / other,
            y = self.y / other,
            z = self.z / other,
            w = self.w / other,
        )


    #---------------------------------------------------------------
    def __rtruediv__(self, other:Number) -> namedtuple:
        return pow(self, -1) * other


    #---------------------------------------------------------------
    def __floordiv__(self, other:Number) -> namedtuple:
        return type(self)(
            x = self.x // other,
            y = self.y // other,
            z = self.z // other,
            w = self.w // other,
        )


    #---------------------------------------------------------------
    def __mod__(self, other:Number) -> namedtuple:
        return type(self)(
            x = self.x % other,
            y = self.y % other,
            z = self.z % other,
            w = self.w % other,
        )


    #---------------------------------------------------------------
    def __divmod__(self, other:Number) -> namedtuple:
        return self // other, self % other


    #---------------------------------------------------------------
    def __pow__(self, other:Number) -> namedtuple:
        return type(self)(
            x = pow(self.x, other) if self.x else 0,
            y = pow(self.y, other) if self.y else 0,
            z = pow(self.z, other) if self.z else 0,
            w = pow(self.w, other) if self.w else 0,
        )


    #---------------------------------------------------------------
    def __lshift__(self, other:Number) -> namedtuple:
        t = type(other)
        return type(self)(
            x = int(self.x) << other,
            y = int(self.y) << other,
            z = int(self.z) << other,
            w = int(self.w) << other,
        )


    #---------------------------------------------------------------
    def __rshift__(self, other:Number) -> namedtuple:
        return type(self)(
            x = int(self.x) >> other,
            y = int(self.y) >> other,
            z = int(self.z) >> other,
            w = int(self.w) >> other,
        )


    #---------------------------------------------------------------
    def __and__(self, other:(Number, tuple)) -> namedtuple:
        cls = type(self)
        if isinstance(other, tuple) and len(other) <= 4:
            other += (0, 0, 0, 0)
            return cls(
                x = int(self.x) & int(other[0]),
                y = int(self.y) & int(other[1]),
                z = int(self.z) & int(other[2]),
                w = int(self.w) & int(other[3]),
            )

        elif isinstance(other, Number):
            return cls(
                x = int(self.x) & other,
                y = int(self.y) & other,
                z = int(self.z) & other,
                w = int(self.w) & other,
            )

        raise TypeError

    __rand__ = __and__


    #---------------------------------------------------------------
    def __or__(self, other:(Number, tuple)) -> namedtuple:
        cls = type(self)
        if isinstance(other, tuple) and len(other) <= 4:
            other += (0, 0, 0, 0)
            return cls(
                x = int(self.x) | int(other[0]),
                y = int(self.y) | int(other[1]),
                z = int(self.z) | int(other[2]),
                w = int(self.w) | int(other[3]),
            )

        elif isinstance(other, Number):
            return cls(
                x = int(self.x) | other,
                y = int(self.y) | other,
                z = int(self.z) | other if self.z else 0,
                w = int(self.w) | other if self.w else 0,
            )

        raise TypeError

    __ror__ = __or__


    #---------------------------------------------------------------
    def __xor__(self, other:(Number, tuple)) -> namedtuple:
        cls = type(self)
        if isinstance(other, tuple) and len(other) <= 4:
            other += (0, 0, 0, 0)
            return cls(
                x = int(self.x) ^ int(other[0]),
                y = int(self.y) ^ int(other[1]),
                z = int(self.z) ^ int(other[2]) if self.z or other[2] else 0,
                w = int(self.w) ^ int(other[3]) if self.w or other[3] else 0,
            )

        elif isinstance(other, Number):
            return cls(
                x = int(self.x) ^ other,
                y = int(self.y) ^ other,
                z = int(self.z) ^ other if self.z else 0,
                w = int(self.w) ^ other if self.w else 0,
            )

        raise TypeError

    __rxor__ = __xor__
