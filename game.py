"""
Game window is 1600x900
"""

from tkinter import *
from datetime import date
from math import floor

from typing import Optional


tk = Tk()

UPDATE_INTERVAL = int(1000/60)  # 60 fps
DRAW_INTERVAL = int(1000/60)  # 60 fps

COLOR_GREEN = "#151f13"


class Game:
    # time in milliseconds between each zombie spawn
    ZOMBIE_SPAWN_COOLDOWN: int = 500

    def __init__(self, master):
        self.tk = master
        self.tk.geometry("1600x900")
        self.tk.resizable(False, False)

        self.canvas = Canvas(self.tk, width=1280, height=720, bg=COLOR_GREEN, cursor="hand2", highlightthickness=0)
        self.canvas.pack(expand=YES, fill=BOTH)

        self.started = False
        self.isGameOver: bool = False
        self.username = "User"

        self.sprites: List[ISprite] = []
        self.bullets = None
        self.player = None
        self.zombies = None
        self.score: int = 0
        self.scoreIndicator = None
        self.pausedIndicator = None
        self.bossKeyBg = None
        self.targetNumZombies: float = 0
        self.dontSpawnZombie: bool = True
        self.updateScheduled: bool = False
        self.drawScheduled: bool = False
        self.paused: bool = True

        self.font = "Helvetica 15"
        self.usernameInput = Entry(self.tk, width=23, font=self.font, justify=CENTER, bg="white")
        self.usernameInput.bind("<Return>", lambda e: self.submitUsername())
        self.usernameBtn = Button(self.tk, text="Start", bg="white", fg=COLOR_GREEN, font=self.font, command=self.submitUsername)
        self.canvas.create_text(800, 400, text="Please enter a username", fill="white", font=self.font)
        self.canvas.create_window(800, 450, window=self.usernameInput)
        self.canvas.create_window(800, 510, window=self.usernameBtn)

        tk.bind('<Escape>', lambda e: self.togglePaused())
        tk.bind('<Control-Escape>', lambda e: self.toggleBossKey())
        tk.bind('<Return>', lambda e: self.restart())

    def start(self):
        self.started = True

        self.canvas.delete('all')
        for sprite in self.sprites:
            del sprite

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

        self.paused = False

    def restart(self):
        if not self.isGameOver:
            return
        else:
            self.start()

    def submitUsername(self):
        username = self.usernameInput.get()
        if len(username) == 0:
            self.usernameInput.configure(bg="red")
            self.tk.after(300, lambda: self.usernameInput.configure(bg="white"))
            return
        self.username = username
        self.paused = False

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
        if not self.started:
            if not paused:
                self.start()
            return
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

        self.sprites.append(Leaderboard(self.score, date.today().strftime("%d-%m-%Y"), self.username))
        self.scoreIndicator.position = ScoreIndicator.POS_GAMEOVER


if __name__ == "__main__":
    from assets.ISprite import ISprite
    from assets.Sprite import Sprite
    from assets.SpriteGroup import SpriteGroup
    from assets.Vectors import Vector2

    from Sprites.Bullet import Bullets
    from Sprites.HealthIndicator import HealthIndicator
    from Sprites.Leaderboard import Leaderboard
    from Sprites.Player import Player
    from Sprites.ScoreIndicator import ScoreIndicator
    from Sprites.Zombie import Zombie

    from typing import List

    game = Game(tk)
    game.tk.mainloop()
