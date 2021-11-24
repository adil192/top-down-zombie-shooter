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
        self.maxHearts: int = self.player.hearts  # assume player starts at max health

        self.drawnHearts: int = 0
        self.canvas_hearts: list = []

    def first_draw(self, canvas: Canvas):
        super(HealthIndicator, self).first_draw(canvas)
        self.canvas_hearts = []
        x = 20
        for i in range(self.maxHearts):
            image = HEART_FULL if self.player.hearts > i else HEART_BROKEN
            self.canvas_hearts.append(canvas.create_image(x, 20, image=image, anchor=NW))
            x += HEART_SIZE + HEART_PADDING
        self.drawnHearts = self.player.hearts

    def redraw(self, canvas: Canvas):
        super(HealthIndicator, self).redraw(canvas)
        if self.player.hearts != self.drawnHearts:  # player's hp changed
            self.undraw(canvas)
            self.first_draw(canvas)

    def undraw(self, canvas: Canvas):
        super(HealthIndicator, self).undraw(canvas)
        for heart in self.canvas_hearts:
            canvas.delete(heart)
