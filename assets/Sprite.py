from math import sin, cos, pi, atan2
from tkinter import PhotoImage, Canvas, NW

from assets.Vectors import Vector2

from typing import Union


class Sprite:
    def __init__(self, image: Union[str, PhotoImage]):
        """
        :param image: This must either be a filepath to an image,
            or the PhotoImage itself.
        """
        if isinstance(image, str):
            self.image = PhotoImage(file=image)
        else:
            self.image = image
        self.imageSize = Vector2(self.image.width(), self.image.height())
        self.position = Vector2(0, 0)
        self.rotation = 0

    @property
    def position(self):
        return self._pos

    @position.setter
    def position(self, new: Vector2):
        self._pos = new
        self.centrePosition = new - self.imageSize / 2

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
        self._forwards = new
        self._rotation = atan2(new.x, new.y)

    def update(self, dt):
        """
        :param dt: time since last update in seconds
        """
        pass

    def draw(self, canvas: Canvas):
        canvas.create_image(self.centrePosition.x, self.centrePosition.y, image=self.image, anchor=NW)
