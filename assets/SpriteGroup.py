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

    def draw(self, canvas: Canvas):
        for child in self.children:
            child.draw(canvas)
