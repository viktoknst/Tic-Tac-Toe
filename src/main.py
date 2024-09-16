from src.app.tic_tac_toe_board import TikTacToeBoard
from src.app.tic_tac_toe_game import TicTacToeGame
import asyncio
import threading


def main():
    game = TicTacToeGame()
    board = TikTacToeBoard(game)
    uri = "ws://localhost:8000/ws"
    threading.Thread(target=lambda:
                     asyncio.run(board.connect_to_server(uri))).start()
    board.mainloop()


if __name__ == "__main__":
    main()
