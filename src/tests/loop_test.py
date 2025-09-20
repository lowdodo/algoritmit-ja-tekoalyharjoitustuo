import unittest
from gameloop import GameLoop

class TestGameLoop(unittest.TestCase):
    def setUp(self):
        self.game_loop = GameLoop()
        # Disable random tile addition for deterministic results
        self.game_loop.game.add_tile = lambda: None

    def test_apply_move_invalid_direction(self):
        self.game_loop.game.board = [
            [2, 0, 2, 4],
            [4, 4, 0, 0],
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ]
        moved = self.game_loop.apply_move("invalid_direction")
        self.assertFalse(moved)
        # Board should remain unchanged
        expected = [
            [2, 0, 2, 4],
            [4, 4, 0, 0],
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ]
        self.assertEqual(self.game_loop.game.board, expected)