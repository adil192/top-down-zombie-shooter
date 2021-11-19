from dataclasses import dataclass


@dataclass
class Vector2:
    x: float = 0
    y: float = 0

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
