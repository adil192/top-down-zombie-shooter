from math import sin, cos, atan2
from tkinter import Canvas

from assets.Vectors import Vector2


class ISprite:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.position = Vector2(0, 0)
        self.rotation: float = 0
        self._hidden: bool = False
        self.destroyed: bool = False
        self.needsANewDraw = True

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

    def first_draw(self):
        self.needsANewDraw = False
        pass

    def redraw(self):
        if self.needsANewDraw:
            self.undraw()
            self.first_draw()
        pass

    def undraw(self):
        pass

    @property
    def hidden(self):
        return self._hidden

    @hidden.setter
    def hidden(self, hidden: bool):
        if self._hidden == hidden:
            return  # not changed, don't do anything
        self._hidden = hidden
        if hidden:
            self.undraw()
        else:
            self.first_draw()
