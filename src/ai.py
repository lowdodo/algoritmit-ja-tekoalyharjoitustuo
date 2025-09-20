from copy import deepcopy
from game2048 import Game2048


class AI2048:
    def __init__(self, game: Game2048 = None, depth: int = 2):
        self.depth = depth
        self.game = game

    @staticmethod
    def evaluate_board(board):
        # heuristic to favor board with more empty tiles and higher biggest tile
        empty_tiles = sum(row.count(0) for row in board)
        max_tile = max(max(row) for row in board)
        return max_tile + empty_tiles * 10

    def expectiminimax(self, game: Game2048, depth: int = None, direction=None):
        if depth is None:
            depth = self.depth

        if depth == 0 or game.is_game_over():
            return self.evaluate_board(game.board), direction

        if direction is not None:
            new_game = deepcopy(game)
            old_board = deepcopy(new_game.board)

            if direction == 'left':
                new_board = new_game.move_left()
            elif direction == 'right':
                new_board = new_game.move_right()
            elif direction == 'up':
                new_board = new_game.move_up()
            elif direction == 'down':
                new_board = new_game.move_down()
            else:
                raise ValueError("Invalid direction")

            if new_board == old_board:
                return float('-inf'), None

            new_game.board = new_board
            new_game.add_tile()
            return self.expectiminimax(new_game, depth - 1)[0], direction

        total_score = 0
        empty_tiles = [(row, colum) for row in range(game.size)
                       for colum in range(game.size) if game.board[row][colum] == 0]
        num_empty = len(empty_tiles)

        for row, colum in empty_tiles:
            for tile_value, probability in [(2, 0.9), (4, 0.1)]:
                new_game = deepcopy(game)
                new_game.board[row][colum] = tile_value
                score, _ = self.expectiminimax(new_game, depth - 1)
                total_score += (score * probability) / num_empty

        return total_score, direction

    def best_move(self, game: Game2048 = None, depth: int = None):
        if game is None:
            game = self.game
        if depth is None:
            depth = self.depth

        moves = ['left', 'right', 'up', 'down']
        best_score = float('-inf')
        best_direction = None

        for move in moves:
            score, _ = self.expectiminimax(game, depth, move)
            if score > best_score:
                best_score, best_direction = score, move

        if best_score == float('-inf'):
            return None

        return best_direction
