from tkinter import Canvas

from assets.SpriteGroup import SpriteGroup
from assets.Sprite import Sprite
from assets.Vectors import Vector2

from Sprites.Zombie import Zombie

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game import Game


class Bullets(SpriteGroup):
    def __init__(self, game: "Game"):
        super().__init__(game.canvas)
        self.game: Game = game

    def newBullet(self, startPos: Vector2, forwards: Vector2) -> "_Bullet":
        bullet = _Bullet(self.canvas, startPos, forwards, self.game)
        self.children.insertRight(bullet)
        return bullet


class _Bullet(Sprite):
    # bullet speed in pixels per second
    SPEED: float = (1600**2 + 900**2) ** 0.5

    COLLIDER_WIDTH: float = 20  # wider than the actual image (6px x 6px) since the bullet is quite fast

    def __init__(self, canvas: Canvas, startPos: Vector2, forwards: Vector2, game: "Game"):
        super(_Bullet, self).__init__(canvas, "images/bullet.png")
        self.position = startPos
        self.forwards = forwards
        self.game: Game = game

    def update(self, dt):
        super(_Bullet, self).update(dt)

        if self.hidden:
            return

        self.position += self.forwards * (self.__class__.SPEED / 60)

        sqr_collision_threshold = (Zombie.COLLIDER_WIDTH + self.__class__.COLLIDER_WIDTH) ** 2
        zombie: Zombie
        for zombie in self.game.zombies.children:
            if (zombie.position - self.position).sqrMagnitude < sqr_collision_threshold:
                # collision
                killed = zombie.shot()
                if killed:
                    self.game.OnZombieKilled()
                self.destroy()

    def destroy(self):
        self.destroyed = True

    def validatePosition(self):
        if self.position.x < 0 or self.position.x > 1600 or self.position.y < 0 or self.position.y > 900:
            self.destroy()
