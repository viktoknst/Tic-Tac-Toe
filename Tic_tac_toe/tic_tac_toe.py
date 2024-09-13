import tkinter as tk
from tkinter import font
from typing import NamedTuple
from itertools import cycle
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
        # This function sets up the internal representation of the board as a 2D grid of Move objects.
        # It also precomputes all possible ways a player can win, which will be used later to check for winning conditions during the game.
        self._current_moves = []

        for row in range(self.board_size):
            current_row = []

            for col in range(self.board_size):
                current_row.append(Move(row, col))
                
            self._current_moves.append(current_row)

        self._winning_combos = self._get_winning_combos()


    def _get_winning_combos(self):
        # This function provides all the possible ways a player can win in the game.
        # zip(*rows) transposes the rows, turning them into columns. It pairs up elements from the same index across all rows, effectively forming the columns of the board.
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
    

    def process_move(self, move):
        # The process_move function performs several key tasks: Update the board, check all possible winning combinations and update the game state.
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        
        for combo in self._winning_combos:
            results = set()

            for n, m in combo:
                results.add(self._current_moves[n][m].label)

            if len(results) == 1 and (Label.NONE not in results):
                self._has_winner = True
                self.winner_combo = combo
                break
    

    def has_winner(self):
        return self._has_winner
    

    def is_tied(self):
        # Checks if the game has finished in a tie
        no_winner = not self._has_winner
        played_moves = []

        for row in self._current_moves:
            for move in row:
                played_moves.append(move.label != Label.NONE)

        return no_winner and all(played_moves)
    

    def toggle_player(self):
        self.current_player = next(self._players)

    
    def reset_game(self):
        # Resets the board and win condition values such as _has_winner and winner_combo and sets new clear values to row_content.
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        
        self._has_winner = False
        self.winner_combo = []


class TikTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tik Tac Toe Board")
        self._cells = {}
        self._game = game
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()

    
    def _create_board_display(self):
        # Creates the window for the game.
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display= tk.Label(
            master = display_frame,
            text = "Make the first move!",
            font = font.Font(size=28, weight="bold")
        )

        self.display.pack()

    
    def _create_board_grid(self):
        # Creates the grid made out of buttons.
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
                    width=5,
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
    


    def _create_menu(self):
        # Creates the drop down menu with the "Play again" and "Exit" functions.
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)

        file_menu.add_command(
            label="Play Again",
            command=self.reset_board
        )

        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="Menu", menu=file_menu)


    def play(self, event):
        # The play function is the core game controller that handles:
        #
        #     - User interaction when clicking on the board.
        #     - Validating and processing moves.
        #     - Checking for a win or tie.
        #     - Updating the game display to reflect the current state of the game (next player's turn, a win, or a tie).

        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        is_free_spot = self._game._current_moves[row][col].label == Label.NONE

        if is_free_spot and not self._game._has_winner:
            move = Move(row, col, self._game.current_player.label)

            self._update_button(clicked_btn)
            self._game.process_move(move)

            if self._game.has_winner():
                self._highlight_cells()
                msg = f'Player "{self._game.current_player.label.value}" won!'
                color = self._game.current_player.color
                self._update_display(msg, color)
                return

            if self._game.is_tied():
                self._update_display(msg="Tied game!", color="red")
                return

            self._game.toggle_player()
            msg = f"{self._game.current_player.label.value}'s turn"
            self._update_display(msg)
            
    
    def _update_button(self, clicked_btn):
        # Updates the buttons so they show their new label
        clicked_btn.config(text=self._game.current_player.label.value)
        clicked_btn.config(fg=self._game.current_player.color)

    
    def _update_display(self, msg, color="black"):
        # Updates messages
        self.display["text"] = msg
        self.display["fg"] = color

    
    def _highlight_cells(self):
        # At the end of the game the winning cells are highlighted. This function is responsible for that.
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="black")
            

    def reset_board(self):
        # Resets the board after "Play again" has been selected in the menu.
        self._game.reset_game()
        self._update_display(msg="Ready?")

        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")


def main():
    game = TicTacToeGame()
    board = TikTacToeBoard(game)
    board.mainloop()


if __name__ == "__main__":
    main()