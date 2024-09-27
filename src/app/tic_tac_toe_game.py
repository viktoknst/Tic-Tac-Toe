import os
from src.app.definitions import DEFAULT_PLAYERS, BOARD_SIZE, Move, Label
from itertools import cycle
from pymongo import MongoClient
from dotenv import load_dotenv


# The TicTacToeGame class is responsible for managing the game state
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
        load_dotenv()

        # MongoDB setup
        MONGODB_URI = os.getenv("MONGODB_URI")

        self.mongo_client = MongoClient(MONGODB_URI)
        self.db = self.mongo_client["tic_tac_toe_db"]
        self.collection = self.db["game_state"]

    def clear_database(self):
        """Clear the MongoDB database."""
        self.collection.delete_many({})

    def save_move_to_db(self, move):
        """Save the move to the MongoDB database."""
        self.collection.replace_one(
            # TODO: use ids to host different games
            {"_id": 1},  # Use a constant ID to always replace the last move
            {
                "row": move.row,
                "col": move.col,
                "label": move.label.value,
            },
            upsert=True
        )

    def load_last_move_from_db(self):
        """Load the last move from the MongoDB database."""
        last_move = self.collection.find_one({"_id": 1})
        if last_move:
            return Move(
                row=last_move["row"],
                col=last_move["col"],
                label=Label(last_move["label"])
            )
        return None

    def _setup_board(self):
        """Setup the game board."""
        self._current_moves = []
        for row in range(self.board_size):
            current_row = []
            for col in range(self.board_size):
                current_row.append(Move(row, col))
            self._current_moves.append(current_row)
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self):
        """Get all possible winning combinations."""
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
        """Process a move and check if there is a winner."""
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
        """Check if there is a winner."""
        return self._has_winner

    def is_spot_free(self, row, col):
        """Check if a spot is free."""
        return self._current_moves[row][col].label == Label.NONE

    def is_tied(self):
        """Check if the game is tied."""
        no_winner = not self._has_winner
        played_moves = []
        for row in self._current_moves:
            for move in row:
                played_moves.append(move.label != Label.NONE)

        return no_winner and all(played_moves)

    def toggle_player(self):
        """Toggle the current player."""
        self.current_player = next(self._players)

    def get_players(self):
        """Get the players."""
        return DEFAULT_PLAYERS

    def get_winner_combo(self):
        """Get the winning combination."""
        return self.winner_combo

    def create_move(self, row, col):
        """Create a move."""
        return Move(row, col, self.current_player.label)

    def reset_game(self):
        """Reset the game."""
        # TODO: use id system to delete specific game
        self.clear_database()
        self._setup_board()
        self._has_winner = False
