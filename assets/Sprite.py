from tkinter import PhotoImage, Canvas, NW
from assets.Vectors import Vector2


class Sprite:
    def __init__(self, image_file: str):
        self.image = PhotoImage(file=image_file)
        self.imageSize = Vector2(self.image.width(), self.image.height())
        self.position = Vector2(0, 0)

    @property
    def position(self):
        return self._pos

    @position.setter
    def position(self, new: Vector2):
        self._pos = new
        self.centrePosition = new - self.imageSize / 2

    def draw(self, canvas: Canvas):
        canvas.create_image(self.centrePosition.x, self.centrePosition.y, image=self.image, anchor=NW)
