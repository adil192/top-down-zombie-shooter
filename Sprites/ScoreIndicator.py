from tkinter import Canvas, NE

from assets.ISprite import ISprite

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game import Game


class ScoreIndicator(ISprite):
    def __init__(self, game: "Game"):
        super(ScoreIndicator, self).__init__()
        self.game: "Game" = game

        self.font_size = 30
        self.font = f'Helvetica {self.font_size} bold'

    def draw(self, canvas: Canvas):
        canvas.create_text(1600-20, 0+20, text=self.game.score, fill="white", font=self.font, anchor=NE)
