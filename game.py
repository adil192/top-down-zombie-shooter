"""
Game window is 1600x900
"""

from tkinter import *


tk = Tk()

UPDATE_INTERVAL = int(1000/60)  # 60 fps
DRAW_INTERVAL = int(1000/60)  # 60 fps


class Game:
    def __init__(self, master):
        self.tk = master
        self.tk.geometry("1600x900")
        self.tk.resizable(False, False)

        self.canvas = Canvas(self.tk, width=1280, height=720, bg="#151f13", cursor="hand2")
        self.canvas.pack(expand=YES, fill=BOTH)

        self.sprites: List[ISprite] = []

        self.player = Player()
        self.player.setupKeyBindings(self.tk)
        self.sprites.append(self.player)

        self.zombie = Zombie(self.player)
        self.sprites.append(self.zombie)

        self.sprites.append(HealthIndicator(self.player))

        self.pausedIndicator = Sprite("images/Emojis/23f8.png")
        self.pausedIndicator.position = Vector2(1600, 900) / 2
        self.sprites.append(self.pausedIndicator)
        self.updateScheduled: bool = False
        self.drawScheduled: bool = False
        self.paused = False

        tk.bind('<Escape>', lambda e: self.togglePaused())

    def update(self):
        for sprite in self.sprites:
            sprite.update(UPDATE_INTERVAL / 1000)

        self.updateScheduled = False
        if not self.paused:
            self.updateScheduled = True
            self.tk.after(UPDATE_INTERVAL, self.update)

    def draw(self):
        self.canvas.delete('all')
        for sprite in self.sprites:
            sprite.draw(self.canvas)

        self.drawScheduled = False
        if not self.paused:
            self.drawScheduled = True
            self.tk.after(DRAW_INTERVAL, self.draw)

    def togglePaused(self):
        self.paused = not self.paused

    @property
    def paused(self) -> bool:
        return self.__paused

    @paused.setter
    def paused(self, paused: bool):
        self.__paused = paused
        self.pausedIndicator.hidden = not self.paused
        if not paused:
            if not self.updateScheduled:
                self.updateScheduled = True
                self.update()
            if not self.drawScheduled:
                self.drawScheduled = True
                self.draw()


if __name__ == "__main__":
    from assets.Sprite import Sprite
    from assets.ISprite import ISprite
    from assets.Vectors import Vector2

    from Sprites.HealthIndicator import HealthIndicator
    from Sprites.Player import Player
    from Sprites.Zombie import Zombie

    from typing import List

    game = Game(tk)
    game.tk.mainloop()
