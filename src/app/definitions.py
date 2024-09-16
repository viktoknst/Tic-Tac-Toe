from typing import NamedTuple
from enum import Enum


class Label(Enum):
    X = "X"
    O = "O"
    NONE = ""


class Player(NamedTuple):
    label: Label
    color: str


class Move(NamedTuple):
    row: int
    col: int
    label: Label = Label.NONE


BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label=Label.O, color="green"),
    Player(label=Label.X, color="gold")
)