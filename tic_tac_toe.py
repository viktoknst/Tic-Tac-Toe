import tkinter as tk
from tkinter import font
from typing import NamedTuple
from itertools import cycle

#hello

class Player(NamedTuple):
    label: str
    color: str


class Move(NamedTuple):
    row: int
    col: int
    label: str = ""


BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label="X", color="gray"),
    Player(label="O", color="gold")
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
        self._current_moves = []

        for row in range(self.board_size):
            current_row = []

            for col in range(self.board_size):
                current_row.append(Move(row, col))
                
            self._current_moves.append(current_row)

        self._winning_combos = self._get_winning_combos()


    def _get_winning_combos(self):
        rows = []

        for row in self._current_moves:
            current_row = []

            for move in row:
                current_row.append((move.row, move.col))

            rows.append(current_row)

        columns = []
        for col in zip(*rows):
            columns.append(list(col))

        first_diagonal = []
        for i, row in enumerate(rows):
            first_diagonal.append(row[i])

        second_diagonal = []
        for j, col in enumerate(reversed(columns)):
            second_diagonal.append(col[j])

        return rows + columns + [first_diagonal, second_diagonal]
    

    def is_valid_move(self, move):
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner

        return no_winner and move_was_not_played
    

    def process_move(self, move):
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        
        for combo in self._winning_combos:
            results = set()

            for n, m in combo:
                results.add(self._current_moves[n][m].label)

            is_win = (len(results) == 1) and ("" not in results)

            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break
    

    def has_winner(self):
        return self._has_winner
    

    def is_tied(self):
        no_winner = not self._has_winner
        played_moves = []

        for row in self._current_moves:
            for move in row:
                played_moves.append(move.label)

        return no_winner and all(played_moves)
    

    def toggle_player(self):
        self.current_player = next(self._players)


class TikTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tik Tac Toe Board")
        self._cells = {}
        self._game = game
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

        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)

            for col in range(self._game.board_size):
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
                button.bind("<ButtonPress-1>", self.play)
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )
    

    def play(self, event):
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        move = Move(row, col, self._game.current_player.label)

        if self._game.is_valid_move(move):
            self._update_button(clicked_btn)
            self._game.process_move(move)

            if self._game.is_tied():
                self._update_display(msg="Tied game!", color="red")

            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'Player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self._update_display(msg, color)

            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)
            
    
    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)

    
    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    
    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="black")


def main():
    game = TicTacToeGame()
    board = TikTacToeBoard(game)
    board.mainloop()


if __name__ == "__main__":
    main()