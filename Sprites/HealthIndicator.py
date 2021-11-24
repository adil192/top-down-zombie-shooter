from tkinter import PhotoImage, Canvas, NW

from assets.ISprite import ISprite

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Sprites.Player import Player


HEART_SIZE: int = 32
HEART_PADDING: int = 5
HEART_FULL: PhotoImage = PhotoImage(file="images/Emojis/2764.png")
HEART_BROKEN: PhotoImage = PhotoImage(file="images/Emojis/1f494.png")


class HealthIndicator(ISprite):
    def __init__(self, canvas: Canvas, player: "Player"):
        super().__init__(canvas)
        self.player: "Player" = player
        self.maxHearts: int = self.player.hearts  # assume player starts at max health

        self.drawnHearts: int = 0
        self.canvas_hearts: list = []

    def first_draw(self):
        super(HealthIndicator, self).first_draw()
        self.canvas_hearts = []
        x = 20
        for i in range(self.maxHearts):
            image = HEART_FULL if self.player.hearts > i else HEART_BROKEN
            self.canvas_hearts.append(self.canvas.create_image(x, 20, image=image, anchor=NW))
            x += HEART_SIZE + HEART_PADDING
        self.drawnHearts = self.player.hearts

    def redraw(self):
        super(HealthIndicator, self).redraw()
        if self.player.hearts != self.drawnHearts:  # player's hp changed
            self.undraw()
            self.first_draw()

    def undraw(self):
        super(HealthIndicator, self).undraw()
        for heart in self.canvas_hearts:
            self.canvas.delete(heart)
