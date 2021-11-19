"""
Game window is 1280x720
"""

from tkinter import *


class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.geometry("1280x720")

        self.canvas = Canvas(self.tk, width=1280, height=720)
        self.canvas.pack(expand=YES, fill=BOTH)


if __name__ == "__main__":
    game = Game()
    game.tk.mainloop()
