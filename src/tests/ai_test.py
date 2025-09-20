import unittest
from ai import AI2048
from game2048 import Game2048


class TestAI2048(unittest.TestCase):
    def setUp(self):
        return super().setUp()

    def test_best_move_returns_valid_direction(self):
        game = Game2048()
        game.board = [
            [2, 0, 2, 4],
            [4, 4, 0, 0],
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ]
        ai = AI2048(game)
        move = ai.best_move()
        self.assertIn(move, ['left', 'right', 'up', 'down'])

    def test_expectiminimax_evaluates_board(self):
        game = Game2048()
        game.board = [
            [2, 0, 2, 4],
            [4, 4, 0, 0],
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ]
        ai = AI2048(game)
        score, _ = ai.expectiminimax(game, depth=1)
        self.assertIsInstance(score, (int, float))

    def test_depth_none(self):
        game = Game2048()
        game.board = [
            [2, 0, 2, 4],
            [4, 4, 0, 0],
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ]
        ai = AI2048(game)
        score, _ = ai.expectiminimax(game, depth=None)
        self.assertIsInstance(score, (int, float))
