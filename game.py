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

        self.sprites: List[Sprite] = []

        self.player = Player()
        self.player.setupKeyBindings(self.tk)
        self.sprites.append(self.player)

        self.zombie = Zombie()
        self.sprites.append(self.zombie)

        self.update()
        self.draw()

    def update(self):
        for sprite in self.sprites:
            sprite.update(UPDATE_INTERVAL / 1000)

        self.tk.after(UPDATE_INTERVAL, self.update)

    def draw(self):
        self.canvas.delete('all')
        
        for sprite in self.sprites:
            sprite.draw(self.canvas)

        self.tk.after(DRAW_INTERVAL, self.draw)


if __name__ == "__main__":
    from assets.Sprite import Sprite
    from assets.Vectors import Vector2

    from Sprites.Player import Player
    from Sprites.Zombie import Zombie

    from typing import List

    game = Game(tk)
    game.tk.mainloop()
