from dataclasses import dataclass


@dataclass
class Vector2:
    x: float = 0
    y: float = 0

    @property
    def sqrMagnitude(self):
        return self.x ** 2 + self.y ** 2

    @property
    def magnitude(self):
        return self.sqrMagnitude ** 0.5

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector2(self.x * other.x, self.y * other.y)

    def __pow__(self, other):
        return Vector2(self.x ** other.x, self.y ** other.y)

    def __truediv__(self, other):
        return Vector2(self.x / other.x, self.y / other.y)

    def __floordiv__(self, other):
        return Vector2(self.x // other.x, self.y // other.y)

    def __mod__(self, other):
        return Vector2(self.x % other.x, self.y % other.y)
