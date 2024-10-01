import random
from src.app.definitions import Move, Label


class Bot:
    """Simple bot that makes random moves."""
    def __init__(self, game, label=Label.o):
        self._game = game
        self.label = label

    def make_move(self):
        """Bot selects a random free spot on the board."""
        available_moves = [
            (row, col)
            for row in range(self._game.board_size)
            for col in range(self._game.board_size)
            if self._game.is_spot_free(row, col)
        ]
        if available_moves:
            row, col = random.choice(available_moves)
            return Move(row, col, self.label)
        return None
