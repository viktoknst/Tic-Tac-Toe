import tkinter as tk
from tkinter import font
from typing import NamedTuple
from itertools import cycle

class Player(NamedTuple):
    label: str
    color: str


class Move(NamedTuple):
    row: int
    col: int
    label: str = ""


BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label="X", color="green"),
    Player(label="O", color="blue")
)


class TicTacToeGame:
    def __init__(self, players = DEFAULT_PLAYERS, board_size = BOARD_SIZE):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()

    
    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()


    def _get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]

        return rows + columns + [first_diagonal, second_diagonal]
    

    def is_valid_move(self, move):
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label = ""
        no_winner = not self._has_winner

        return no_winner and move_was_not_played
    

    def process_move(self, move):
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        
        for combo in self._winning_combos:
            results = set(
                self._current_moves[n][m].label
                for n, m in combo
            )
            is_win = (len(results) == 1) and ("" not in results)

            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break
    

    def has_winner(self):
        return self._has_winner
    

    def is_tied(self):
        no_winner = not self._has_winner
        played_moves = (
            move.label for row in self._current_moves for move in row
        )
        return no_winner and all(played_moves)
    

    def toggle_player(self):
        self.current_player = next(self._players)


class TikTacToeBoard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tik Tac Toe Board")
        self._cells = {}
        self._create_board_display()
        self._create_board_grid()

    
    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display= tk.Label(
            master = display_frame,
            text = "Make the first move!",
            font = font.Font(size=28, weight="bold")
        )

        self.display.pack()

    
    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        number_of_rows = 3
        number_of_cols = 3

        for row in range(number_of_rows):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)

            for col in range(number_of_cols):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    height=2,
                    width=4,
                    highlightbackground="lightblue"
                )

                self._cells[button] = (row, col)
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )


def main():
    board = TikTacToeBoard()
    board.mainloop()


if __name__ == "__main__":
    main()