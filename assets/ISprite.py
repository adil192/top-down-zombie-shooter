from math import sin, cos, pi, atan2
from tkinter import PhotoImage, Canvas, NW

from assets.Vectors import Vector2


class ISprite:
    def __init__(self):
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

    def first_draw(self, canvas: Canvas):
        self.needsANewDraw = False
        pass

    def redraw(self, canvas: Canvas):
        if self.needsANewDraw:
            self.undraw(canvas)
            self.first_draw(canvas)
        pass

    def undraw(self, canvas: Canvas):
        pass

    @property
    def hidden(self):
        return self._hidden

    def setHidden(self, canvas: Canvas, hidden: bool):
        if self._hidden == hidden:
            return  # not changed, don't do anything
        self._hidden = hidden
        if hidden:
            self.undraw(canvas)
        else:
            self.first_draw(canvas)
