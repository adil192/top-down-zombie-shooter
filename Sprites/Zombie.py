from math import pi, sin, cos, atan2
from tkinter import Tk, PhotoImage

from assets.AnimatedSprite import AnimatedSprite
from assets.Vectors import Vector2

from typing import List


class Zombie(AnimatedSprite):
    FRAMES_ATTACK: List[PhotoImage] =\
        AnimatedSprite.getFramesWithFilePattern("images/Top_Down_Zombie/skeleton-attack_{0}.png")
    FRAMES_IDLE: List[PhotoImage] =\
        AnimatedSprite.getFramesWithFilePattern("images/Top_Down_Zombie/skeleton-idle_{0}.png")
    FRAMES_MOVE: List[PhotoImage] =\
        AnimatedSprite.getFramesWithFilePattern("images/Top_Down_Zombie/skeleton-move_{0}.png")

    MAX_SPEED: float = 50

    def __init__(self):
        super().__init__(self.__class__.FRAMES_MOVE)
        self.position = Vector2(1600 - self.halfImageSize.x, 0.5 * 900)
        self.rotation = -pi / 2
        self.speed = self.__class__.MAX_SPEED  # pixels per second

        self.walkingRotation: float = -pi / 2
        self.walkingDirection: Vector2 = Vector2(-1, 0)

        self.inputUp = 0
        self.inputDown = 0
        self.inputLeft = 1
        self.inputRight = 0

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, new):
        self._speed = new
        self.cycleLength = 2

    def update(self, dt):
        super(self.__class__, self).update(dt)

        # translate input into walking direction
        dx = self.inputRight - self.inputLeft
        dy = self.inputDown - self.inputUp
        self.walkingRotation = atan2(dx, dy)
        self.walkingDirection = Vector2(sin(self.walkingRotation), cos(self.walkingRotation))

        # point zombie in direction of movement
        self.rotation = self.walkingRotation

        # move
        self.position += self.walkingDirection * (self.speed * dt)

        if dx == 0 and dy == 0:
            if self.speed == 0 and (self.frames != self.__class__.FRAMES_IDLE and self.frames != self.__class__.FRAMES_ATTACK):
                self.frames = self.__class__.FRAMES_IDLE
            self.speed = 0
        else:
            if self.speed > 0:
                self.frames = self.__class__.FRAMES_MOVE
            self.speed = self.__class__.MAX_SPEED
