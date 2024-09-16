'''
File that tests functions from app
'''

import sys
sys.path.append('/home/vkonstantinov/Tic_tac_toe')
from src.app.tic_tac_toe_game import TicTacToeGame
from src.app.definitions import Move, Label
import pytest

class TestGame():
    def test_setup_board(self):
        game = TicTacToeGame(board_size=3)
        game._setup_board()

        assert len(game._current_moves) == 3

        for row in game._current_moves:
            assert len(row) == 3
            for move in row:
                assert isinstance(move, Move)

        for i, row in enumerate(game._current_moves):
            for j, move in enumerate(row):
                assert move.row == i
                assert move.col == j

        expected_winning_combos = [
            # Rows
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            # Columns
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            # Diagonals
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],
        ]

        assert game._winning_combos == expected_winning_combos


    def test_get_winning_combos(self):
        game = TicTacToeGame(board_size=3)
        game._setup_board()
        winning_combos = game._get_winning_combos()

        expected_combos = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],

            # Columns
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],

            # Diagonals
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)]            
        ]

        assert winning_combos == expected_combos


    def test_process_move_no_winner(self):
        game = TicTacToeGame(board_size=3)
        game._setup_board()

        move = Move(row=0, col=0, label=Label.O)
        game.process_move(move)

        assert game._current_moves[0][0].label == Label.O
        assert not game.has_winner()


    def test_process_move_winner(self):
        game = TicTacToeGame(board_size=3)
        game._setup_board()

        game.process_move(Move(row=0, col=0, label=Label.O))
        game.process_move(Move(row=0, col=1, label=Label.O))
        game.process_move(Move(row=0, col=2, label=Label.O))

        assert game.has_winner() == True
        assert game.winner_combo == [(0, 0), (0, 1), (0, 2)]


    def test_process_move_tie(self):
        game = TicTacToeGame(board_size=3)
        game._setup_board()

        moves = [
            Move(0, 0, Label.O), Move(0, 1, Label.X), Move(0, 2, Label.O),
            Move(1, 0, Label.X), Move(1, 1, Label.O), Move(1, 2, Label.X),
            Move(2, 0, Label.X), Move(2, 1, Label.O), Move(2, 2, Label.X)
        ]

        for move in moves:
            game.process_move(move)

        assert not game.has_winner()
        assert game.is_tied() == True

    
    def test_has_winner_initial_state(self):
        game = TicTacToeGame(board_size=3)
        game._setup_board()
        assert game.has_winner() is False


    def test_has_winner_after_winning_move(game):
        game = TicTacToeGame(board_size=3)
        game._setup_board()

        game._current_moves[0][0] = Move(0, 0, Label.X)
        game._current_moves[0][1] = Move(0, 1, Label.X)
        game._current_moves[0][2] = Move(0, 2, Label.X)

        game._has_winner = True

        assert game.has_winner() is True


    def test_is_tied(self):
        game = TicTacToeGame(board_size=3)
        game._setup_board()

        moves = [
            Move(0, 0, Label.O), Move(0, 1, Label.X), Move(0, 2, Label.O),
            Move(1, 0, Label.X), Move(1, 1, Label.O), Move(1, 2, Label.X),
            Move(2, 0, Label.X), Move(2, 1, Label.O), Move(2, 2, Label.X)
        ]

        for move in moves:
            game.process_move(move)

        assert game.is_tied() == True
        assert not game.has_winner()

    
    def test_reset_game(self):
        game = TicTacToeGame(board_size=3)
        game._setup_board()

        moves = [
            Move(0, 0, Label.O), Move(0, 1, Label.O), Move(0, 2, Label.O),
            Move(1, 0, Label.X), Move(1, 1, Label.X), Move(1, 2, Label.X),
            Move(2, 0, Label.O), Move(2, 1, Label.NONE), Move(2, 2, Label.NONE)
        ]
        for move in moves:
            game.process_move(move)

        assert game.has_winner() == True
        assert game.winner_combo != []

        game.reset_game()

        for row in game._current_moves:
            for move in row:
                assert move.label == Label.NONE

        assert game.has_winner() == False
        assert game.winner_combo == []