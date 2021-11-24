from tkinter import Canvas

from assets.ISprite import ISprite


class SpriteGroup(ISprite):
    """
    SpriteGroup is a virtual sprite object that contains a number of sprites in the scene.
    """

    def __init__(self):
        super().__init__()
        self.children = []

    def update(self, dt):
        self.children = [child for child in self.children if not child.destroyed]

        for child in self.children:
            child.update(dt)

    def first_draw(self, canvas: Canvas):
        super(SpriteGroup, self).first_draw(canvas)
        for child in self.children:
            child.first_draw(canvas)

    def redraw(self, canvas: Canvas):
        super(SpriteGroup, self).redraw(canvas)
        for child in self.children:
            child.redraw(canvas)

    def undraw(self, canvas: Canvas):
        for child in self.children:
            child.undraw(canvas)
