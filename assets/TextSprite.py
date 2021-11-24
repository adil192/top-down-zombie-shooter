from tkinter import Canvas

from assets.ISprite import ISprite


class TextSprite(ISprite):
    def __init__(self, text: str = ""):
        self.text = text
        self.options = {
            "fill": "white",
            "font": "Helvetica 16 bold"
        }
        self.canvas_text = "None"

        super(TextSprite, self).__init__()

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, new: str):
        self.__text = new
        self.needsANewDraw = True

    def first_draw(self, canvas: Canvas):
        super(TextSprite, self).first_draw(canvas)
        self.canvas_text = canvas.create_text(*self.position, text=self.text, **self.options)

    def redraw(self, canvas: Canvas):
        super(TextSprite, self).redraw(canvas)
        pass
    
    def undraw(self, canvas: Canvas):
        super(TextSprite, self).undraw(canvas)
        canvas.delete(self.canvas_text)
