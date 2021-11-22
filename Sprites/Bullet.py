from tkinter import Tk

from assets.SpriteGroup import SpriteGroup
from assets.Sprite import Sprite
from assets.Vectors import Vector2

from Sprites.Zombie import Zombie

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game import Game


class Bullets(SpriteGroup):
    def __init__(self, game: "Game"):
        super().__init__()
        self.game: Game = game

    def newBullet(self, startPos: Vector2, forwards: Vector2):
        self.children.append(_Bullet(startPos, forwards, self.game))


class _Bullet(Sprite):
    # bullet is destroyed after LIFETIME milliseconds
    LIFETIME: int = 1000

    # bullet speed in pixels per second
    SPEED: float = (1600**2 + 900**2) ** 0.5

    COLLIDER_WIDTH: float = 50  # wider than the actual image (6px x 6px) since the bullet is quite fast

    def __init__(self, startPos: Vector2, forwards: Vector2, game: "Game"):
        super(_Bullet, self).__init__("images/bullet.png")
        self.position = startPos
        self.forwards = forwards
        self.game: Game = game

        game.tk.after(self.__class__.LIFETIME, self.destroy)

    def update(self, dt):
        super(_Bullet, self).update(dt)

        if self.hidden:
            return

        self.position += self.forwards * (self.__class__.SPEED / 60)

        sqr_collision_threshold = Zombie.COLLIDER_WIDTH + self.__class__.COLLIDER_WIDTH
        zombie: Zombie
        for zombie in self.game.zombies.children:
            if (zombie.position - self.position).sqrMagnitude < sqr_collision_threshold:
                # collision
                zombie.shot()
                self.destroy()

    def destroy(self):
        self.destroyed = True
