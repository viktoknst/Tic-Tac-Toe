from src.app.definitions import DEFAULT_PLAYERS, BOARD_SIZE, Move, Label
from itertools import cycle

class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
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