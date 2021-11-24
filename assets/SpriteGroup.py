from tkinter import Canvas

from assets.ISprite import ISprite
from assets.LinkedList import LinkedList


class SpriteGroup(ISprite):
    """
    SpriteGroup is a virtual sprite object that contains a number of sprites in the scene.
    """

    def __init__(self, canvas: Canvas):
        super().__init__(canvas)
        self.children: LinkedList = LinkedList()

    def update(self, dt):
        self.children.removeWith(
            shouldRemove=lambda node: node.element.destroyed,
            onRemove=lambda child: self.removeChild(child),
            removeAll=True
        )

        for child in self.children:
            child.update(dt)

    def removeChild(self, child: ISprite):
        child.hidden = True

    def first_draw(self):
        super(SpriteGroup, self).first_draw()
        for child in self.children:
            child.first_draw()

    def redraw(self):
        super(SpriteGroup, self).redraw()
        for child in self.children:
            child.redraw()

    def undraw(self):
        for child in self.children:
            child.undraw()
