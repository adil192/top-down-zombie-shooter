"""
Leaderboard stored as
{score}, {date}, {name}
"""

from tkinter import Canvas

from assets.ISprite import ISprite

from typing import Union, List, Tuple


class Leaderboard(ISprite):
    FILE = "leaderboard.txt"
    MAX_RECORDS = 5

    TITLE = "Leaderboard"
    HEADER_NUM = "#"
    HEADER_SCORE = "Score"
    HEADER_DATE = "Date"
    HEADER_NAME = "Name"

    def __init__(self, canvas: Canvas,  newScore: int = None, newDate: str = None, newName: str = None):
        super().__init__(canvas)

        leaderboard = sorted(Leaderboard.getLeaderboard(), key=lambda x: x[0], reverse=True)  # sort desc by score

        if newScore is not None:
            leaderboard = self.addToLeaderboard(leaderboard, newScore, newDate, newName)

        self.lines = [
            Leaderboard._formatRow(Leaderboard.HEADER_NUM, Leaderboard.HEADER_SCORE, Leaderboard.HEADER_DATE, Leaderboard.HEADER_NAME)
        ]
        for i in range(len(leaderboard)):
            self.lines.append(Leaderboard._formatRow(i+1, *leaderboard[i]))

        self.line_padding = 20
        self.font_size = 20
        self.font = f'Monospace {self.font_size} bold'

        self.canvas_texts = []

    def addToLeaderboard(self, leaderboard: List[tuple], newScore: int, newDate: str, newName: str):
        # if new score should be on the leaderboard
        if len(leaderboard) < Leaderboard.MAX_RECORDS or newScore > leaderboard[-1][0]:
            # we don't want duplicate records, so remove a pre-existing record for this user if it exists
            for line in leaderboard:
                if line[-1].lower() == newName.lower():
                    if newScore <= line[0]:
                        return leaderboard
                    else:
                        leaderboard.remove(line)
                        break

            newLine = (newScore, newDate, newName)
            for i in range(len(leaderboard)):
                if leaderboard[i][0] < newScore:
                    leaderboard.insert(i, newLine)  # insert at right place in sorted list
                    break
            else:
                leaderboard.append(newLine)
            leaderboard = leaderboard[:Leaderboard.MAX_RECORDS]  # only keep the best 5
            Leaderboard.writeLeaderboard(leaderboard)  # save to txt file
        return leaderboard

    def first_draw(self):
        super(Leaderboard, self).first_draw()

        self.canvas_texts = []

        x = 1600*0.5
        y = 900*0.4

        self.canvas_texts.append(self.canvas.create_text(x, y, text=Leaderboard.TITLE.ljust(len(self.lines[0])), fill="white", font=self.font))
        y += self.font_size + self.line_padding

        for i in range(len(self.lines)):
            self.canvas_texts.append(self.canvas.create_text(x, y, text=self.lines[i], fill="white", font=self.font))
            y += self.font_size + self.line_padding

    def redraw(self):
        super(Leaderboard, self).redraw()
        # assume we never need to update the leaderboard after it's been first_draw()ed
        pass

    def undraw(self):
        super(Leaderboard, self).undraw()
        for canvas_text in self.canvas_texts:
            self.canvas.delete(canvas_text)

    @staticmethod
    def _formatRow(n: Union[int, str], score: Union[int, str], date: str, name: str):
        if n == "#":
            return f"| {n} | {score:<10} |{date:^14}| {name:>17} |"
        return f"| {n} |  {score:<9} |{date:^14}| {name:>16}  |"

    @staticmethod
    def parseLeaderboardLine(line: str) -> (Union[int, str], str, str):
        parts = line.split(", ", maxsplit=2)  # using `maxsplit=2` means we don't need to remove commas from name
        score = int(parts[0])
        date = parts[1]
        name = parts[2]
        return score, date, name

    @classmethod
    def getLeaderboard(cls):
        try:
            with open(cls.FILE) as f:
                return [cls.parseLeaderboardLine(line.strip()) for line in f.readlines()]
        except FileNotFoundError:
            return []

    @classmethod
    def writeLeaderboard(cls, leaderboard: List[Tuple[int, str, str]]):
        lines = [f"{score}, {date}, {name}\r\n" for (score, date, name) in leaderboard]
        with open(cls.FILE, "w") as f:
            f.writelines(lines)
