import tkinter as tk
import threading
from time import sleep
from tkinter import font
from src.app.definitions import Move, Label


class TikTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tik Tac Toe Board")
        self._cells = {}
        self._game = game
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()

        thread = threading.Thread(
            target=self._poll_database_for_updates, daemon=True
        )
        thread.start()

    def _poll_database_for_updates(self):
        """Poll MongoDB for any updates in the game state."""
        while True:
            sleep(1)  # Poll every second
            last_move = self._game.load_last_move_from_db()
            if last_move:
                self._update_board_with_move(last_move)

    def _update_board_with_move(self, move):
        """Update the board with a move from the database."""
        for button, (row, col) in self._cells.items():
            if (row, col) == (move.row, move.col):
                button.config(text=move.label.value)
                break

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Make the first move!",
            font=font.Font(size=28, weight="bold"),
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
                    width=5,
                    highlightbackground="lightblue",
                )
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def _create_menu(self):
        # Creates the drop down menu
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="Play Again", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="Menu", menu=file_menu)

    def play(self, event):
        # The play function is the core game controller that handles:
        #
        #     - User interaction when clicking on the board.
        #     - Validating and processing moves.
        #     - Checking for a win or tie.
        #     - Updating the game display to reflect the current state
        #       of the game (next player's turn, a win, or a tie).

        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        is_free_spot = self._game._current_moves[row][col].label == Label.NONE

        if is_free_spot and not self._game._has_winner:
            move = Move(row, col, self._game.current_player.label)
            self._update_button(clicked_btn)
            self._game.process_move(move)

            self._game.save_move_to_db(move)

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
        # At the end of the game the winning cells are highlighted.
        # This function is responsible for that.
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
