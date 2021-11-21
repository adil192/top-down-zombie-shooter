from math import sin, cos, pi, atan2
from tkinter import PhotoImage, Canvas, NW

from assets.Vectors import Vector2


class ISprite:
    def __init__(self):
        self.position = Vector2(0, 0)
        self.rotation: float = 0
        self.hidden: bool = False

    @property
    def position(self):
        return self._pos

    @position.setter
    def position(self, new: Vector2):
        self._pos = new

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, new: float):
        self._rotation = new
        self._forwards = Vector2(sin(new), cos(new))

    @property
    def forwards(self) -> Vector2:
        return self._forwards

    @forwards.setter
    def forwards(self, new: Vector2):
        self._forwards = new.normalise()
        self._rotation = atan2(new.x, new.y)

    def update(self, dt):
        """
        :param dt: time since last update in seconds
        """
        pass

    def draw(self, canvas: Canvas):
        if self.hidden:
            return
