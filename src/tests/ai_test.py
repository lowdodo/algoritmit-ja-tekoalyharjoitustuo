import unittest
from ai import AI2048
from game2048 import Game2048


class TestAI2048Extended(unittest.TestCase):
    def setUp(self):
        self.game = Game2048()
        # Disable random tile addition for deterministic tests
        self.game.add_tile = lambda: None

    def test_best_move_returns_valid_direction(self):
        self.game.board = [
            [2, 0, 2, 4],
            [4, 4, 0, 0],
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ]
        ai = AI2048(self.game, depth=1)
        move = ai.best_move()
        self.assertIn(move, ['left', 'right', 'up', 'down'],
                      f"AI returned invalid move: {move}")

    def test_expectiminimax_returns_numeric_score(self):
        self.game.board = [
            [2, 0, 2, 4],
            [4, 4, 0, 0],
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ]
        ai = AI2048(self.game, depth=1)
        score, _ = ai.expectiminimax(self.game, depth=1)
        self.assertIsInstance(score, (int, float))

    def test_ai_chooses_none_if_no_moves(self):
        self.game.board = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2]
        ]
        ai = AI2048(self.game, depth=1)
        move = ai.best_move()
        self.assertIsNone(
            move, "AI should return None when no moves are possible")

    def test_ai_chooses_only_valid_move(self):
        self.game.board = [
            [2, 2, 4, 8],
            [16, 32, 64, 128],
            [256, 512, 1024, 2048],
            [4096, 8192, 16384, 32768]
        ]
        ai = AI2048(self.game, depth=1)
        move = ai.best_move()
        self.assertEqual(
            move, 'left', "AI should choose the only possible merging move")

    def test_ai_with_default_depth(self):
        self.game.board = [
            [2, 0, 2, 4],
            [4, 4, 0, 0],
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ]
        ai = AI2048(self.game)
        score, _ = ai.expectiminimax(self.game, depth=ai.depth)
        self.assertIsInstance(score, (int, float))


if __name__ == "__main__":
    unittest.main()
