"""
Game window is 1600x900
"""

from tkinter import *
from math import floor


tk = Tk()

UPDATE_INTERVAL = int(1000/60)  # 60 fps
DRAW_INTERVAL = int(1000/60)  # 60 fps


class Game:
    # time in milliseconds between each zombie spawn
    ZOMBIE_SPAWN_COOLDOWN: int = 500

    def __init__(self, master):
        self.tk = master
        self.tk.geometry("1600x900")
        self.tk.resizable(False, False)

        self.canvas = Canvas(self.tk, width=1280, height=720, bg="#151f13", cursor="hand2")
        self.canvas.pack(expand=YES, fill=BOTH)

        self.isGameOver: bool = False

        self.sprites: List[ISprite] = []

        self.bullets = Bullets(self)
        self.sprites.append(self.bullets)

        self.player = Player(self, self.bullets)
        self.player.setupKeyBindings()
        self.sprites.append(self.player)

        self.zombies = SpriteGroup()
        self.sprites.append(self.zombies)

        self.sprites.append(HealthIndicator(self.player))

        self.score: int = 0
        self.scoreIndicator = ScoreIndicator(self)
        self.sprites.append(self.scoreIndicator)

        self.pausedIndicator = Sprite("images/Emojis/23f8.png")
        self.pausedIndicator.position = Vector2(1600, 900) / 2
        self.sprites.append(self.pausedIndicator)

        self.bossKeyBg = Sprite("images/BossKeyBg.png")
        self.bossKeyBg.position = Vector2(1600, 900) / 2
        self.sprites.append(self.bossKeyBg)

        self.targetNumZombies: float = 2.75
        self.dontSpawnZombie: bool = False

        self.updateScheduled: bool = False
        self.drawScheduled: bool = False
        self.paused = False

        tk.bind('<Escape>', lambda e: self.togglePaused())
        tk.bind('<Control-Escape>', lambda e: self.toggleBossKey())

    def update(self):
        for sprite in self.sprites:
            sprite.update(UPDATE_INTERVAL / 1000)

        if not self.dontSpawnZombie and len(self.zombies.children) < self.targetNumZombies - 1:
            self.zombies.children.append(Zombie(self.player))
            self.dontSpawnZombie = True
            self.tk.after(self.__class__.ZOMBIE_SPAWN_COOLDOWN, self._unlockZombieSpawn)

        self.updateScheduled = False
        if not self.paused:
            self.updateScheduled = True
            self.tk.after(UPDATE_INTERVAL, self.update)

    def _unlockZombieSpawn(self):
        self.dontSpawnZombie = False

    def draw(self):
        self.canvas.delete('all')
        for sprite in self.sprites:
            sprite.draw(self.canvas)

        self.drawScheduled = False
        if not self.paused:
            self.drawScheduled = True
            self.tk.after(DRAW_INTERVAL, self.draw)

    def OnZombieKilled(self):
        self.targetNumZombies += 0.25
        self.score += 1

    def togglePaused(self):
        self.paused = not self.paused

    def toggleBossKey(self):
        if self.paused:
            self.paused = False
        else:
            self.paused = True
            self.pausedIndicator.hidden = True
            self.bossKeyBg.hidden = False

    @property
    def paused(self) -> bool:
        return self.__paused

    @paused.setter
    def paused(self, paused: bool):
        self.__paused = paused
        self.pausedIndicator.hidden = not self.paused
        self.bossKeyBg.hidden = True
        if not paused:
            if not self.updateScheduled:
                self.updateScheduled = True
                self.update()
            if not self.drawScheduled:
                self.drawScheduled = True
                self.draw()

    def onGameOver(self):
        if self.isGameOver:
            return

        self.isGameOver = True
        self.paused = True
        self.pausedIndicator.hidden = True


if __name__ == "__main__":
    from assets.Sprite import Sprite
    from assets.SpriteGroup import SpriteGroup
    from assets.ISprite import ISprite
    from assets.Vectors import Vector2

    from Sprites.Bullet import Bullets
    from Sprites.HealthIndicator import HealthIndicator
    from Sprites.Player import Player
    from Sprites.ScoreIndicator import ScoreIndicator
    from Sprites.Zombie import Zombie

    from typing import List

    game = Game(tk)
    game.tk.mainloop()
