"""
Game window is 1600x900
"""
from hashlib import sha1
from tkinter import *
from datetime import date
import pickle

tk = Tk()

from assets.ISprite import ISprite
from assets.SavedState import SavedState
from assets.Sprite import Sprite
from assets.SpriteGroup import SpriteGroup
from assets.TextSprite import TextSprite
from assets.Vectors import Vector2

from Sprites.Bullet import Bullets
from Sprites.HealthIndicator import HealthIndicator
from Sprites.Leaderboard import Leaderboard
from Sprites.Player import Player
from Sprites.ScoreIndicator import ScoreIndicator
from Sprites.Zombie import Zombie

from typing import List


UPDATE_INTERVAL = int(1000/60)  # 60 fps
REDRAW_INTERVAL = int(1000/60)  # 60 fps

COLOR_GREEN = "#151f13"

IGNORED_KEYSYMS = ["Tab", "Alt_L", "Alt_R", "Shift_L", "Shift_R", "BackSpace"]  # ignore these keys when choosing controls
ARROW_KEYSYMS = ["Up", "Left", "Down", "Right"]  # the direction keys
ARROW_KEYSYMS_REPR = ["⯅", "⯇", "⯆", "⯈"]  # the direction keys


def keysymToSymbol(keysym: str):
    if keysym in ARROW_KEYSYMS:
        return ARROW_KEYSYMS_REPR[ARROW_KEYSYMS.index(keysym)]
    if len(keysym) == 1 and keysym.islower():
        return keysym.upper()
    return keysym


SAVE_FILE = "saves/save_{}.bin"


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
        self.controls: List[str] = ["w", "a", "s", "d"]

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
        self.redrawScheduled: bool = False
        self.paused: bool = True

        self.createForm()

        tk.bind('<Escape>', lambda e: self.togglePaused())
        tk.bind('<Control-Escape>', lambda e: self.toggleBossKey())
        tk.bind('<Return>', lambda e: self.restart())
        tk.protocol("WM_DELETE_WINDOW", self.onClose)

    # noinspection PyAttributeOutsideInit
    def createForm(self):
        font = "Helvetica 15"

        self.canvas.create_text(800, 500, text="Please enter a username", fill="white", font=font)

        self.usernameInput = Entry(self.tk, width=23, font=font, justify=CENTER, bg="white")
        self.usernameInput.bind("<Return>", lambda e: self.submitForm())
        self.canvas.create_window(800, 550, window=self.usernameInput)

        self.usernameBtn = Button(self.tk, text="Start", bg="white", fg=COLOR_GREEN, font="Helvetica 30", command=self.submitForm)
        self.canvas.create_window(800, 650, window=self.usernameBtn)

        self.controlsInputs = []
        controlsInputsPositions = (
            (800, 150),
            (700, 250),
            (800, 250),
            (900, 250),
        )
        for i in range(len(self.controls)):
            entry = Entry(self.tk, width=2, font="Helvetica 50", justify=CENTER, bg="white")
            entry.insert(0, keysymToSymbol(self.controls[i]))
            entry.configure(state="readonly")
            entry.bind("<KeyPress>", lambda e, entry=entry: self.controlsInputKeypress(entry, e))
            entry.keysym = self.controls[i]
            self.controlsInputs.append(entry)
            self.canvas.create_window(*controlsInputsPositions[i], window=entry)

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

        self.zombies = SpriteGroup(self.canvas)
        self.sprites.append(self.zombies)

        self.sprites.append(HealthIndicator(self.canvas, self.player))

        self.score: int = 0
        self.scoreIndicator = ScoreIndicator(self)
        self.sprites.append(self.scoreIndicator)

        self.pausedIndicator = Sprite(self.canvas, "images/Emojis/23f8.png")
        self.pausedIndicator.position = Vector2(1600, 900) / 2
        self.sprites.append(self.pausedIndicator)

        self.bossKeyBg = Sprite(self.canvas, "images/BossKeyBg.png")
        self.bossKeyBg.position = Vector2(1600, 900) / 2
        self.bossKeyBg.hidden = True
        self.sprites.append(self.bossKeyBg)

        self.targetNumZombies: float = 2.75
        self.dontSpawnZombie: bool = False

        self.loadState()

        self.paused = False

    def restart(self):
        if not self.isGameOver:
            return
        else:
            self.start()

    def submitForm(self):
        if self.started:
            return

        username = self.usernameInput.get()
        if len(username) == 0:
            self.usernameInput.configure(bg="red")
            self.tk.after(300, lambda: self.usernameInput.configure(bg="white"))
            return
        self.username = username

        self.controls = [entry.keysym for entry in self.controlsInputs]

        self.paused = False

    def controlsInputKeypress(self, entry: Entry, e):
        keysym = e.keysym
        if keysym in IGNORED_KEYSYMS:
            return

        if len(keysym) == 1:
            # if it's uppercase, the player would need to hold shift for every control
            # so make it lowercase
            keysym = keysym.lower()
        entry.keysym = keysym
        entry.configure(state=NORMAL)
        entry.delete(0, END)
        entry.insert(0, keysymToSymbol(keysym))
        entry.configure(state="readonly")

    def update(self):
        for sprite in self.sprites:
            sprite.update(UPDATE_INTERVAL / 1000)

        if not self.dontSpawnZombie and len(self.zombies.children) < self.targetNumZombies - 1:
            self.zombies.children.insertRight(Zombie(self.canvas, self.player))
            self.dontSpawnZombie = True
            self.tk.after(self.__class__.ZOMBIE_SPAWN_COOLDOWN, self._unlockZombieSpawn)

        self.updateScheduled = False
        if not self.paused:
            self.updateScheduled = True
            self.tk.after(UPDATE_INTERVAL, self.update)

    def _unlockZombieSpawn(self):
        self.dontSpawnZombie = False

    def redraw(self):
        for sprite in self.sprites:
            sprite.redraw()

        self.redrawScheduled = False
        if not self.paused:
            self.redrawScheduled = True
            self.tk.after(REDRAW_INTERVAL, self.redraw)

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
            if not self.redrawScheduled:
                self.redrawScheduled = True
                self.redraw()

    @property
    def usernameHash(self):
        return self._usernameHash

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, new: str):
        self._username = new
        self._usernameHash = sha1(self._username.encode("utf-8")).hexdigest()

    def onGameOver(self):
        if self.isGameOver:
            return

        self.isGameOver = True
        self.paused = True
        self.pausedIndicator.hidden = True

        self.sprites.append(Leaderboard(self.canvas, self.score, date.today().strftime("%d-%m-%Y"), self.username))
        self.scoreIndicator.position = ScoreIndicator.POS_GAMEOVER

        hintText = TextSprite(self.canvas, text="Press Enter to play again!")
        hintText.position = Vector2(1600*0.5, 900*0.8)
        self.sprites.append(hintText)

    def saveState(self):
        savedState: SavedState = SavedState(
            score=self.score,
            hearts=self.player.hearts,
            playerPosition=self.player.position,
            zombiePositions=[zombie.position for zombie in self.zombies.children],
            zombieHearts=[zombie.hearts for zombie in self.zombies.children],
            controls=self.controls
        )
        with open(SAVE_FILE.format(self.usernameHash), "wb") as save_file:
            pickle.dump(savedState, save_file)

    def loadState(self):
        try:
            with open(SAVE_FILE.format(self.usernameHash), "rb") as save_file:
                savedState: SavedState = pickle.load(save_file)
        except FileNotFoundError:
            return

        self.score = savedState.score
        self.player.hearts = savedState.hearts
        self.player.position = savedState.playerPosition

        self.zombies.undraw()
        index = self.sprites.index(self.zombies)
        self.zombies = SpriteGroup(self.canvas)
        self.sprites[index] = self.zombies
        for i in range(len(savedState.zombiePositions)):
            zombie: Zombie = Zombie(self.canvas, self.player)
            zombie.position = savedState.zombiePositions[i]
            zombie.hearts = savedState.zombieHearts[i]
            self.zombies.children.insertRight(zombie)

    def onClose(self):
        self.saveState()
        self.tk.destroy()


if __name__ == "__main__":
    game = Game(tk)
    tk.mainloop()
