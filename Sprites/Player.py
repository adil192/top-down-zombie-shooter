from math import pi, sin, cos, atan2
from tkinter import PhotoImage
from enum import Enum, auto as enum_next

from assets.AnimatedSprite import AnimatedSprite
from assets.Vectors import Vector2
from Sprites.Bullet import Bullets

from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from game import Game
    from Sprites.Bullet import _Bullet


class _Gun(Enum):
    Handgun = enum_next()
    Shotgun = enum_next()


class Player(AnimatedSprite):
    FRAMES_IDLE_HANDGUN: List[PhotoImage] =\
        AnimatedSprite.getFramesWithFilePattern("images/Top_Down_Survivor/handgun/idle/survivor-idle_handgun_{0}.png")
    FRAMES_MOVE_HANDGUN: List[PhotoImage] =\
        AnimatedSprite.getFramesWithFilePattern("images/Top_Down_Survivor/handgun/move/survivor-move_handgun_{0}.png")
    FRAMES_IDLE_SHOTGUN: List[PhotoImage] =\
        AnimatedSprite.getFramesWithFilePattern("images/Top_Down_Survivor/shotgun/idle/survivor-idle_shotgun_{0}.png")
    FRAMES_MOVE_SHOTGUN: List[PhotoImage] =\
        AnimatedSprite.getFramesWithFilePattern("images/Top_Down_Survivor/shotgun/move/survivor-move_shotgun_{0}.png")

    MAX_SPEED: float = 100  # pixels per second
    COLLIDER_WIDTH: float = 50

    def __init__(self, game: "Game", bullets: Bullets):
        super().__init__(game.canvas, self.__class__.FRAMES_IDLE_HANDGUN)
        self.game: Game = game
        self.bullets: Bullets = bullets

        self.position = Vector2(self.halfImageSize.x, 0.5 * 900)
        self.rotation = pi / 2
        self.max_speed = self.__class__.MAX_SPEED  # pixels per second
        self.speed = 0  # pixels per second

        self.hearts = 5

        self.walkingRotation: float = pi / 2
        self.walkingDirection: Vector2 = Vector2(1, 0)

        self.inputUp = 0
        self.inputDown = 0
        self.inputLeft = 0
        self.inputRight = 0
        self.mousePos = Vector2(0.7, 0.5) * Vector2(1600, 900)

        self.gun: _Gun = _Gun.Handgun

        self.setupKeyBindings()
        self.activeCheatCodes: List[str] = []

    def setupKeyBindings(self):
        controls = self.game.controls
        inputs = ("up", "left", "down", "right")
        # e.g. self.game.tk.bind("<KeyPress-w>", lambda e: self.setInput(up=1))
        for i in range(len(inputs)):
            self.game.tk.bind(f"<KeyPress-{controls[i]}>",
                              lambda e, kwarg=inputs[i]: self.setInput(**{kwarg: 1}))
            self.game.tk.bind(f"<KeyRelease-{controls[i]}>",
                              lambda e, kwarg=inputs[i]: self.setInput(**{kwarg: 0}))

        self.game.tk.bind('<Motion>', lambda e: self.setInput(mouse=Vector2(e.x, e.y)))
        self.game.tk.bind("<Button-1>", lambda e: self.shoot())

        self.game.tk.bind('quick', lambda e: self.cheatCode("quick"))
        self.game.tk.bind('ohno', lambda e: self.cheatCode("ohno"))

    def setInput(self, up: int = None, down: int = None, left: int = None, right: int = None, mouse: Vector2 = None):
        if up is not None:
            self.inputUp = up
        if down is not None:
            self.inputDown = down
        if left is not None:
            self.inputLeft = left
        if right is not None:
            self.inputRight = right
        if mouse is not None:
            self.mousePos = mouse

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, new):
        self._speed = new
        self.cycleLength = max(1, new / 100)

    @property
    def gun(self) -> _Gun:
        return self._gun

    @gun.setter
    def gun(self, gun: _Gun):
        self._gun = gun
        if gun == _Gun.Handgun:
            self.framesIdle = self.__class__.FRAMES_IDLE_HANDGUN
            self.framesMove = self.__class__.FRAMES_MOVE_HANDGUN
        elif gun == _Gun.Shotgun:
            self.framesIdle = self.__class__.FRAMES_IDLE_SHOTGUN
            self.framesMove = self.__class__.FRAMES_MOVE_SHOTGUN

    def shoot(self):
        if self.game.paused:
            return

        bulletDirection = self.mousePos - self.position
        if self.gun == _Gun.Shotgun:
            for i in range(3):
                bullet: "_Bullet" = self.bullets.newBullet(self.position, bulletDirection)
                bullet.rotation += (i-1) * 0.1  # bullets are 0.1 radians apart
        else:
            self.bullets.newBullet(self.position, bulletDirection)

    def update(self, dt):
        super(self.__class__, self).update(dt)

        # translate input into walking direction
        dx = self.inputRight - self.inputLeft
        dy = self.inputDown - self.inputUp
        self.walkingRotation = atan2(dx, dy)
        self.walkingDirection = Vector2(sin(self.walkingRotation), cos(self.walkingRotation))

        # point player in direction of mouse
        self.forwards = self.mousePos - self.position

        # move
        self.position += self.walkingDirection * (self.speed * dt)

        if dx == 0 and dy == 0:
            if self.speed == 0:
                self.frames = self.framesIdle
            self.speed = 0
        else:
            if self.speed > 0:
                self.frames = self.framesMove
            self.speed = self.max_speed

    def cheatCode(self, code: str, reverse: bool = False):
        if (code in self.activeCheatCodes) != reverse:
            return
        if reverse:
            self.activeCheatCodes.remove(code)
        else:
            self.activeCheatCodes.append(code)

        duration: int = 3000
        if code == "quick":
            self.max_speed = self.__class__.MAX_SPEED * (1 if reverse else 2)
            duration = 3000
        elif code == "ohno":
            self.gun = _Gun.Handgun if reverse else _Gun.Shotgun
            duration = 3000
        else:
            return

        if not reverse:
            self.game.tk.after(duration, lambda: self.cheatCode(code, reverse=True))

    def attacked(self):
        self.hearts -= 1
        if self.hearts <= 0:
            self.game.onGameOver()
            self.destroyed = True
