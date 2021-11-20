from math import pi, atan2
from tkinter import Tk, PhotoImage

from assets.AnimatedSprite import AnimatedSprite
from assets.Vectors import Vector2

from typing import List


class Player(AnimatedSprite):
    FRAMES_IDLE: List[PhotoImage] =\
        AnimatedSprite.getFramesWithFilePattern("images/Top_Down_Survivor/handgun/idle/survivor-idle_handgun_{0}.png")
    FRAMES_MOVE: List[PhotoImage] =\
        AnimatedSprite.getFramesWithFilePattern("images/Top_Down_Survivor/handgun/move/survivor-move_handgun_{0}.png")
    MAX_SPEED: float = 50

    def __init__(self):
        super().__init__(Player.FRAMES_IDLE)
        self.position = Vector2(0, 250)
        self.rotation = pi / 2
        self.speed = 50  # pixels per second

        self.inputUp = 0
        self.inputDown = 0
        self.inputLeft = 0
        self.inputRight = 0

    def setupKeyBindings(self, tk: Tk):
        tk.bind("<KeyPress-w>", lambda e: self.setInput(up=1))
        tk.bind("<KeyRelease-w>", lambda e: self.setInput(up=0))
        tk.bind("<KeyPress-s>", lambda e: self.setInput(down=1))
        tk.bind("<KeyRelease-s>", lambda e: self.setInput(down=0))
        tk.bind("<KeyPress-a>", lambda e: self.setInput(left=1))
        tk.bind("<KeyRelease-a>", lambda e: self.setInput(left=0))
        tk.bind("<KeyPress-d>", lambda e: self.setInput(right=1))
        tk.bind("<KeyRelease-d>", lambda e: self.setInput(right=0))

    def setInput(self, up: int = None, down: int = None, left: int = None, right: int = None):
        if up is not None:
            self.inputUp = up
        if down is not None:
            self.inputDown = down
        if left is not None:
            self.inputLeft = left
        if right is not None:
            self.inputRight = right

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, new):
        self._speed = new
        self.cycleLength = max(1, new / 100)

    def update(self, dt):
        super(Player, self).update(dt)
        self.position += self.forwards * (self.speed * dt)

        dx = self.inputRight - self.inputLeft
        dy = self.inputDown - self.inputUp
        self.rotation = atan2(dx, dy)
        if dx == 0 and dy == 0:
            if self.speed == 0:
                self.frames = Player.FRAMES_IDLE
            self.speed = 0
        else:
            if self.speed > 0:
                self.frames = Player.FRAMES_MOVE
            self.speed = Player.MAX_SPEED
