"""
Game window is 1280x720
"""

from tkinter import *
from assets.Sprite import Sprite
from assets.Vectors import Vector2

from typing import List


UPDATE_INTERVAL = int(1000/60)  # 60 fps
DRAW_INTERVAL = int(1000/60)  # 60 fps


class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.geometry("1280x720")
        self.tk.resizable(False, False)

        self.canvas = Canvas(self.tk, width=1280, height=720, bg="#151f13", cursor="hand2")
        self.canvas.pack(expand=YES, fill=BOTH)

        self.sprites: List[Sprite] = []

        self.player = Sprite("images/Top_Down_Survivor/handgun/idle/survivor-idle_handgun_0.png")
        self.sprites.append(self.player)

        self.update()
        self.draw()

    def update(self):
        self.player.position += Vector2(1, 1)

        self.tk.after(UPDATE_INTERVAL, self.update)

    def draw(self):
        self.canvas.delete('all')
        
        for sprite in self.sprites:
            sprite.draw(self.canvas)

        self.tk.after(DRAW_INTERVAL, self.draw)


if __name__ == "__main__":
    game = Game()
    game.tk.mainloop()
