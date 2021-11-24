from math import sin, cos, pi, atan2
from tkinter import PhotoImage, Canvas, NW

from assets.ISprite import ISprite
from assets.Vectors import Vector2

from typing import Union


class Sprite(ISprite):
    def __init__(self, canvas: Canvas, image: Union[str, PhotoImage]):
        """
        :param image: This must either be a filepath to an image,
            or the PhotoImage itself.
        """
        self.halfImageSize = Vector2(0, 0)
        super().__init__(canvas)

        if isinstance(image, str):
            self.image = PhotoImage(file=image)
        else:
            self.image = image

        self.canvas_image = "None"

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, new: PhotoImage):
        self.__image = new
        self.halfImageSize = Vector2(new.width() / 2, new.height() / 2)
        self.topLeftPosition = self.position - self.halfImageSize
        self.needsANewDraw = True

    @ISprite.position.setter
    def position(self, new: Vector2):
        ISprite.position.fset(self, new)
        self.topLeftPosition = new - self.halfImageSize

    def first_draw(self):
        if self.hidden:
            return
        super(Sprite, self).first_draw()
        self.canvas_image = self.canvas.create_image(self.topLeftPosition.x, self.topLeftPosition.y, image=self.image, anchor=NW)

    def redraw(self):
        super(Sprite, self).redraw()
        self.canvas.moveto(self.canvas_image, self.topLeftPosition.x, self.topLeftPosition.y)

    def undraw(self):
        super(Sprite, self).undraw()
        self.canvas.delete(self.canvas_image)
