import tkinter as tk
from src.app.tic_tac_toe_game import TicTacToeGame
from src.app.tic_tac_toe_board import TikTacToeBoard


def start_singleplayer():
    """Starts the singleplayer game (for now, same as multiplayer)."""
    game = TicTacToeGame()
    board = TikTacToeBoard(game)
    board.mainloop()


def start_multiplayer():
    """Starts the multiplayer game."""
    game = TicTacToeGame()
    board = TikTacToeBoard(game)
    board.mainloop()


def show_main_menu():
    """Displays the main menu window."""
    menu_window = tk.Tk()
    menu_window.title("Tic Tac Toe - Main Menu")

    # Title
    title_label = tk.Label(
        menu_window,
        text="Tic Tac Toe",
        font=("Helvetica", 50, "bold"),
        pady=100,
        padx=200
    )
    title_label.pack()

    # Developer name
    developer_label = tk.Label(
        menu_window,
        text="Developed by Victorian Konstantinov",
        font=("Helvetica", 20),
        pady=10
    )
    developer_label.pack()

    # Singleplayer Button
    singleplayer_button = tk.Button(
        menu_window,
        text="Singleplayer",
        font=("Helvetica", 24),
        command=lambda: (menu_window.destroy(), start_singleplayer())
    )
    singleplayer_button.pack(pady=10)

    # Multiplayer Button
    multiplayer_button = tk.Button(
        menu_window,
        text="Multiplayer",
        font=("Helvetica", 24),
        command=lambda: (menu_window.destroy(), start_multiplayer())
    )
    multiplayer_button.pack(pady=10)

    menu_window.mainloop()
