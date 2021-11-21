from tkinter import PhotoImage, Canvas, NW

from assets.ISprite import ISprite

from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from Sprites.Player import Player


HEART_SIZE: int = 32
HEART_PADDING: int = 5
HEART_FULL: PhotoImage = PhotoImage(file="images/Emojis/2764.png")
HEART_BROKEN: PhotoImage = PhotoImage(file="images/Emojis/1f494.png")


class HealthIndicator(ISprite):
    def __init__(self, player: "Player"):
        super().__init__()
        self.player: "Player" = player
        self.maxHearts = self.player.hearts  # assume player starts at max health

    def draw(self, canvas: Canvas):
        if self.hidden:
            return
        x = 20
        for i in range(1, self.maxHearts + 1):
            canvas.create_image(x, 20, image=(HEART_FULL if self.player.hearts >= i else HEART_BROKEN), anchor=NW)
            x += HEART_SIZE + HEART_PADDING
