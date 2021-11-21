from math import pi, sin, cos, atan2
from tkinter import Tk, PhotoImage
from enum import Enum, auto as enum_next

from assets.AnimatedSprite import AnimatedSprite
from assets.Vectors import Vector2

from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from Sprites.Player import Player


class ZombiePriority(Enum):
    Moving = enum_next()
    Attacking = enum_next()
    Idle = enum_next()


class Zombie(AnimatedSprite):
    FRAMES_ATTACK: List[PhotoImage] =\
        AnimatedSprite.getFramesWithFilePattern("images/Top_Down_Zombie/skeleton-attack_{0}.png")
    FRAMES_ATTACK_CRITICAL_POINT = 0.55  # the point in the animation when damage is dealt

    FRAMES_IDLE: List[PhotoImage] =\
        AnimatedSprite.getFramesWithFilePattern("images/Top_Down_Zombie/skeleton-idle_{0}.png")
    FRAMES_MOVE: List[PhotoImage] =\
        AnimatedSprite.getFramesWithFilePattern("images/Top_Down_Zombie/skeleton-move_{0}.png")

    MAX_SPEED: float = 50
    COLLIDER_WIDTH: float = 50

    def __init__(self, target_player: "Player"):
        super().__init__(self.__class__.FRAMES_MOVE)
        self.target_player = target_player

        self.position = Vector2(1600 - self.halfImageSize.x, 0.5 * 900)
        self.rotation = -pi / 2
        self.sqrDistToPlayer = 1600
        self.sqrDistToPlayerLimit = (self.__class__.COLLIDER_WIDTH + self.target_player.__class__.COLLIDER_WIDTH) ** 2
        self.speed = self.__class__.MAX_SPEED  # pixels per second
        self.cycleLength = 2

        self.__priority = ZombiePriority.Moving
        self.priority: ZombiePriority = ZombiePriority.Moving

        # has the zombie attacked the player in the current animation cycle (only for ZombiePriority.Attacking)
        self.hasAttacked = False

    @property
    def priority(self) -> ZombiePriority:
        return self.__priority

    @priority.setter
    def priority(self, new: ZombiePriority):
        if self.__priority != new:
            self.cycleTime = 0  # restart animation time if we change it
        self.__priority = new
        if new == ZombiePriority.Moving:
            self.frames = self.__class__.FRAMES_MOVE
        elif new == ZombiePriority.Attacking:
            self.frames = self.__class__.FRAMES_ATTACK
        elif new == ZombiePriority.Idle:
            self.frames = self.__class__.FRAMES_IDLE

    def update(self, dt):
        super(self.__class__, self).update(dt)

        displacement = self.target_player.position - self.position

        # point towards player
        self.forwards = displacement

        # if player is close enough, switch to attacking
        self.sqrDistToPlayer: float = displacement.sqrMagnitude
        if self.sqrDistToPlayer < self.sqrDistToPlayerLimit:
            self.priority = ZombiePriority.Attacking

        if self.priority == ZombiePriority.Moving:
            self.position += self.forwards * (self.speed * dt)
        elif self.priority == ZombiePriority.Attacking:
            if not self.hasAttacked and self.cycleTime >= self.cycleLength * self.__class__.FRAMES_ATTACK_CRITICAL_POINT:
                self.target_player.attacked()
                self.hasAttacked = True

    def cycleEnded(self):
        if self.priority != ZombiePriority.Attacking:
            return

        self.hasAttacked = False

        # check if player has moved away since attack ended,
        # stop attacking if so
        if self.sqrDistToPlayer > self.sqrDistToPlayerLimit:
            self.priority = ZombiePriority.Moving

