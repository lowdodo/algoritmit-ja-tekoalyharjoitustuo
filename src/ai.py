from copy import deepcopy
from game2048 import Game2048


class AI2048:
    '''AI player for 2048 using the Expectiminimax algorithm.
    
    Attributes:
        game (Game2048): The current game state.
        depth (int): The depth to which the expectiminimax algorithm should search.
    '''

    def __init__(self, game: Game2048 = None, depth: int = 2):
        '''Initializor for the AI player.
        
        Args:
            game (Game2048, optional): The current game state. Defaults to a new game.
            depth (int, optional): The depth to which the expectiminimax algorithm should search. Defaults to 2.
        '''
        self.depth = depth
        self.game = game

    @staticmethod
    def evaluate_board(board):
        ''' Simple heuristic function to favor board with more empty tiles and higher biggest tile'''
        empty_tiles = sum(row.count(0) for row in board)
        max_tile = max(max(row) for row in board)
        return max_tile + empty_tiles * 10

    def expectiminimax(self, game, depth):
        ''' Expectiminimax algorithm implementation.'''
        if game.is_game_over():
            return -float('inf'), None
        elif depth <= 0:
            return self.evaluate_board(game.board), None

        if depth != int(depth):
            best_score = -float('inf')
            best_dir = None
            for move_dir in game.directions:
                new_game = deepcopy(game)
                _, moved = new_game.move(move_dir, add_tile=False)
                if not moved:
                    continue
                score, _ = self.expectiminimax(new_game, depth - 0.5)
                if score > best_score:
                    best_score = score
                    best_dir = move_dir
            if best_dir is None:
                return self.evaluate_board(game.board), None
            return best_score, best_dir

        else:
            empty_tiles = [(r, c) for r in range(game.size)
                           for c in range(game.size) if game.board[r][c] == 0]
            if not empty_tiles:
                return self.evaluate_board(game.board), None
            total_score = 0
            num_empty = len(empty_tiles)
            for r, c in empty_tiles:
                for value, prob in [(2, 0.9), (4, 0.1)]:
                    new_game = deepcopy(game)
                    new_game.board[r][c] = value
                    score, _ = self.expectiminimax(new_game, depth - 0.5)
                    total_score += score * prob / num_empty
            # Chance nodes never return a move
            return total_score, None

    def best_move(self, game: Game2048 = None, depth: int = None):
        ''' Determine the best move using the expectiminimax algorithm.'''
        game = game or self.game
        depth = depth or self.depth

        best_score = -float('inf')
        best_direction = None

        for move_dir in game.directions:
            new_game = deepcopy(game)
            _, moved = new_game.move(move_dir, add_tile=False)
            if not moved:
                continue
            score, _ = self.expectiminimax(new_game, depth - 0.5)
            if score > best_score:
                best_score = score
                best_direction = move_dir

        return best_direction
