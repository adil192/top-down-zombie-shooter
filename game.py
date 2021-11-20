"""
Game window is 1280x720
"""

from tkinter import *
from assets.Sprite import Sprite


class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.geometry("1280x720")
        self.tk.resizable(False, False)

        self.canvas = Canvas(self.tk, width=1280, height=720, bg="#151f13", cursor="hand2")
        self.canvas.pack(expand=YES, fill=BOTH)

        self.player = Sprite("images/Top_Down_Survivor/handgun/idle/survivor-idle_handgun_0.png")
        self.player.draw(self.canvas)


if __name__ == "__main__":
    game = Game()
    game.tk.mainloop()
