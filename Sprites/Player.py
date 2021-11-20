from tkinter import PhotoImage

from assets.AnimatedSprite import AnimatedSprite
from assets.Vectors import Vector2

from typing import List


class Player(AnimatedSprite):
    FRAMES: List[PhotoImage] = AnimatedSprite.getFramesWithFilePattern("images/Top_Down_Survivor/handgun/move"
                                                                       "/survivor-move_handgun_{0}.png")

    def __init__(self):
        super().__init__(Player.FRAMES)
        self.position = Vector2(0, 250)
        self.speed = 20  # pixels per second

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, new):
        self._speed = new
        self.cycleLength = max(1, new / 100)

    def update(self, dt):
        super(Player, self).update(dt)
        self.position += Vector2(self.speed * dt, 0 * dt)
