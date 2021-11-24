from tkinter import Canvas, NE

from assets.ISprite import ISprite
from assets.Vectors import Vector2

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game import Game


class ScoreIndicator(ISprite):
    POS_NORMAL = Vector2(1600-20, 0+20)
    POS_GAMEOVER = Vector2(1600*0.5, 900*0.2)

    def __init__(self, game: "Game"):
        super(ScoreIndicator, self).__init__()
        self.game: "Game" = game
        self.score = self.game.score

        self.font = f'Helvetica 30 bold'
        self.position = self.__class__.POS_NORMAL

    @ISprite.position.getter
    def position(self) -> Vector2:
        return ISprite.position.fget(self)

    @ISprite.position.setter
    def position(self, position: Vector2):
        ISprite.position.fset(self, position)
        font_size = 50 if position == self.__class__.POS_GAMEOVER else 30
        self.font = f'Helvetica {font_size} bold'

    def update(self, dt):
        if self.game.player.destroyed:
            return
        self.score = self.game.score

    def draw(self, canvas: Canvas):
        canvas.create_text(*self.position, text=self.score, fill="white", font=self.font, anchor=NE)
