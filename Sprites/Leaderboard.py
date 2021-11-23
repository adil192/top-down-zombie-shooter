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
    HEADER_SCORE = "score"
    HEADER_DATE = "date"
    HEADER_NAME = "name"

    def __init__(self,  newScore: int = None, newDate: str = None, newName: str = None):
        super().__init__()

        leaderboard = sorted(Leaderboard.getLeaderboard(), key=lambda x: x[0], reverse=True)  # sort desc by score

        # if new score should be on the leaderboard
        if newScore is not None and (len(leaderboard) < Leaderboard.MAX_RECORDS or newScore > leaderboard[-1][0]):
            # we don't want duplicate records, so remove a pre-existing record for this user if it exists
            leaderboard = [(score, date, name) for (score, date, name) in leaderboard if name != newName]

            newLine = (newScore, newDate, newName)
            for i in range(len(leaderboard)):
                if leaderboard[i][0] < newScore:
                    leaderboard.insert(i, newLine)  # insert at right place in sorted list
                    break
            else:
                leaderboard.append(newLine)
            leaderboard = leaderboard[:Leaderboard.MAX_RECORDS]  # only keep the best 5
            Leaderboard.writeLeaderboard(leaderboard)  # save to txt file

        self.lines = [
            Leaderboard._formatRow(Leaderboard.HEADER_NUM, Leaderboard.HEADER_SCORE, Leaderboard.HEADER_DATE, Leaderboard.HEADER_NAME)
        ]
        for i in range(len(leaderboard)):
            self.lines.append(Leaderboard._formatRow(i+1, *leaderboard[i]))

        self.line_padding = 20
        self.font_size = 20
        self.font = f'Monospace {self.font_size} bold'

    def draw(self, canvas: Canvas):
        x = 1600*0.5
        y = 900*0.4

        canvas.create_text(x, y, text=Leaderboard.TITLE.ljust(len(self.lines[0])), fill="white", font=self.font)
        y += self.font_size + self.line_padding

        for i in range(len(self.lines)):
            canvas.create_text(x, y, text=self.lines[i], fill="white", font=self.font)
            y += self.font_size + self.line_padding

    @staticmethod
    def _formatRow(n: Union[int, str], score: Union[int, str], date: str, name: str):
        return f"| {n} |{score:^11}|{date:^14}| {name:^15} |"

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
