from tkinter import Canvas

from assets.ISprite import ISprite


class TextSprite(ISprite):
    def __init__(self, canvas: Canvas, text: str = ""):
        self.text = text
        self.options = {
            "fill": "white",
            "font": "Helvetica 16 bold"
        }
        self.canvas_text = "None"

        super(TextSprite, self).__init__(canvas)

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, new: str):
        self.__text = new
        self.needsANewDraw = True

    def first_draw(self):
        super(TextSprite, self).first_draw()
        self.canvas_text = self.canvas.create_text(*self.position, text=self.text, **self.options)

    def redraw(self):
        super(TextSprite, self).redraw()
        pass
    
    def undraw(self):
        super(TextSprite, self).undraw()
        self.canvas.delete(self.canvas_text)
