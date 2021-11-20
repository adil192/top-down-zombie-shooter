from os.path import exists
from math import floor
from tkinter import PhotoImage, Canvas, NW

from assets.Sprite import Sprite
from assets.Vectors import Vector2

from typing import Union, List


class AnimatedSprite(Sprite):
    def __init__(self, frames: Union[List[PhotoImage], str],
                 cycle_length: float = 1, frame_interval: float = 0):
        """
        :param frames: This must either be a PhotoImage list,
            or a filepath that contains a placeholder - {0} - to
            collect all image frames of the animation.
        """
        if isinstance(frames, str):
            self.frames = AnimatedSprite.getFramesWithFilePattern(frames)
        else:
            self.frames = frames

        super().__init__(self.frames[0])
        self.imageSize = Vector2(self.image.width(), self.image.height())
        self.position = Vector2(0, 0)

        self.cycleTime: float = 0
        self.cycleLength = cycle_length
        self.frameInterval = frame_interval

    @property
    def cycleLength(self):
        return self._cycleLength

    @cycleLength.setter
    def cycleLength(self, new):
        if new > 0:
            self._cycleLength = new
            self._frameInterval = new / len(self.frames)

    @property
    def frameInterval(self):
        return self._frameInterval

    @frameInterval.setter
    def frameInterval(self, new):
        if new > 0:
            self._frameInterval = new
            self._cycleLength = new * len(self.frames)

    @property
    def position(self):
        return self._pos

    @position.setter
    def position(self, new: Vector2):
        self._pos = new
        self.centrePosition = new - self.imageSize / 2

    def update(self, dt):
        self.cycleTime += dt
        frame = floor((self.cycleTime * len(self.frames)) / self.cycleLength)
        if frame >= len(self.frames):
            frame = 0
            self.cycleTime = 0
        self.image = self.frames[frame]

    def draw(self, canvas: Canvas):
        canvas.create_image(self.centrePosition.x, self.centrePosition.y, image=self.image, anchor=NW)

    @staticmethod
    def getFramesWithFilePattern(file_pattern: str) -> List[PhotoImage]:
        i = 0
        frames: List[PhotoImage] = []
        while True:
            try:
                file = file_pattern.format(i)
                if not exists(file):
                    break  # reached end of frames
                else:
                    frames.append(PhotoImage(file=file))
            finally:
                i += 1
        return frames
