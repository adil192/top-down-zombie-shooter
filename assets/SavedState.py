from dataclasses import dataclass

from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from assets.Vectors import Vector2


@dataclass
class SavedState:
    score: int
    hearts: int
    playerPosition: "Vector2"
    zombiePositions: List["Vector2"]
    zombieHearts: List[int]
