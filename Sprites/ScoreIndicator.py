from tkinter import Canvas, NE
from enum import Enum, auto as enum_next

from assets.ISprite import ISprite

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game import Game


class ScoreIndicatorPos(Enum):
    TOP_RIGHT = enum_next()
    CENTRE = enum_next()


class ScoreIndicator(ISprite):
    POS_TOP_RIGHT = (1600-20, 0+20)
    POS_CENTRE = (1600*0.5, 900*0.2)

    def __init__(self, game: "Game"):
        super(ScoreIndicator, self).__init__()
        self.game: "Game" = game

        self.font_size = 30
        self.font = f'Helvetica {self.font_size} bold'

        self.score = self.game.score

        self.setPosition(ScoreIndicatorPos.TOP_RIGHT)

    def setPosition(self, position: ScoreIndicatorPos):
        if position == ScoreIndicatorPos.CENTRE:
            self.position = self.__class__.POS_CENTRE
            self.font_size = 50
        else:
            self.position = self.__class__.POS_TOP_RIGHT
            self.font_size = 30
        self.font = f'Helvetica {self.font_size} bold'

    def update(self, dt):
        if self.game.player.destroyed:
            return
        self.score = self.game.score

    def draw(self, canvas: Canvas):
        canvas.create_text(*self.position, text=self.score, fill="white", font=self.font, anchor=NE)
