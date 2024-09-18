from src.app.tic_tac_toe_game import TicTacToeGame
from src.app.tic_tac_toe_board import TikTacToeBoard


def main():
    game = TicTacToeGame()
    board = TikTacToeBoard(game)
    board.mainloop()


if __name__ == "__main__":
    main()
