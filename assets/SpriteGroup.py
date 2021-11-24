from tkinter import Canvas

from assets.ISprite import ISprite


class SpriteGroup(ISprite):
    """
    SpriteGroup is a virtual sprite object that contains a number of sprites in the scene.
    """

        self.children = []
    def __init__(self, canvas: Canvas):
        super().__init__(canvas)

    def update(self, dt):
        self.children = [child for child in self.children if not child.destroyed]

        for child in self.children:
            child.update(dt)

    def first_draw(self):
        super(SpriteGroup, self).first_draw()
        for child in self.children:
            child.first_draw()

    def redraw(self):
        super(SpriteGroup, self).redraw()
        for child in self.children:
            if child is None:
                continue # todo: remove
            child.redraw()

    def undraw(self):
        for child in self.children:
            child.undraw()
