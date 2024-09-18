from src.app.tic_tac_toe_game import TicTacToeGame
from src.app.tic_tac_toe_board import TikTacToeBoard
from src.app.server import start_server
import threading


def main():
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    game = TicTacToeGame()
    board = TikTacToeBoard(game)
    board.mainloop()


if __name__ == "__main__":
    main()
