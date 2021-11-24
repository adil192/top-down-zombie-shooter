from tkinter import Canvas

from assets.ISprite import ISprite


class TextSprite(ISprite):
    def __init__(self, text: str = ""):
        self.text = text
        self.options = {
            "fill": "white",
            "font": "Helvetica 16 bold"
        }

        super(TextSprite, self).__init__()

    def draw(self, canvas: Canvas):
        if self.hidden:
            return
        canvas.create_text(*self.position, text=self.text, **self.options)
