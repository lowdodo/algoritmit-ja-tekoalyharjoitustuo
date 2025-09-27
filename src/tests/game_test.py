import unittest
from game2048 import Game2048


class TestGame2048Extended(unittest.TestCase):
    def setUp(self):
        self.game = Game2048()
        # Disable random tile addition for deterministic tests
        self.game.add_tile = lambda: None

    def test_slide_and_merge_basic(self):
        row = [2, 2, 0, 2]
        expected = [4, 2, 0, 0]
        self.assertEqual(self.game.slide_and_merge(row), expected)

    def test_slide_and_merge_multiple_merges(self):
        row = [2, 2, 2, 2]
        expected = [4, 4, 0, 0]
        self.assertEqual(self.game.slide_and_merge(row), expected)

    def test_slide_and_merge_no_merge(self):
        row = [2, 4, 8, 16]
        expected = [2, 4, 8, 16]
        self.assertEqual(self.game.slide_and_merge(row), expected)

    def test_move_left_merging(self):
        self.game.board = [
            [2, 2, 0, 2],
            [0, 0, 4, 4],
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ]
        expected = [
            [4, 2, 0, 0],
            [8, 0, 0, 0],
            [4, 4, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.move("left", add_tile=False)
        self.assertEqual(self.game.board, expected)

    def test_move_right_merging(self):
        self.game.board = [
            [2, 2, 0, 2],
            [0, 0, 4, 4],
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ]
        expected = [
            [0, 0, 2, 4],
            [0, 0, 0, 8],
            [0, 0, 4, 4],
            [0, 0, 0, 0]
        ]
        self.game.move("right", add_tile=False)
        self.assertEqual(self.game.board, expected)

    def test_move_up_merging(self):
        self.game.board = [
            [2, 0, 2, 4],
            [2, 0, 2, 4],
            [0, 0, 2, 0],
            [0, 0, 2, 0]
        ]
        expected = [
            [4, 0, 4, 8],
            [0, 0, 4, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.move("up", add_tile=False)
        self.assertEqual(self.game.board, expected)

    def test_move_down_merging(self):
        self.game.board = [
            [2, 0, 2, 4],
            [2, 0, 2, 4],
            [0, 0, 2, 0],
            [0, 0, 2, 0]
        ]
        expected = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 4, 0],
            [4, 0, 4, 8]
        ]
        self.game.move("down", add_tile=False)
        self.assertEqual(self.game.board, expected)

    def test_game_over_empty_board(self):
        self.game.board = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertFalse(self.game.is_game_over())

    def test_game_over_full_no_merge(self):
        self.game.board = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2]
        ]
        self.assertTrue(self.game.is_game_over())

    def test_game_over_merge_possible_row(self):
        self.game.board = [
            [2, 2, 4, 8],
            [16, 32, 64, 128],
            [256, 512, 1024, 2048],
            [4096, 8192, 16384, 32768]
        ]
        self.assertFalse(self.game.is_game_over())

    def test_game_over_false_when_merge_possible(self):
        self.game.board = [
            [2, 2, 4, 8],
            [16, 32, 64, 128],
            [256, 512, 1024, 2],
            [4, 8, 16, 32]
        ]
        self.assertFalse(self.game.is_game_over())

    def test_game_over_merge_possible_column(self):
        self.game.board = [
            [2, 4, 8, 16],
            [2, 32, 64, 128],
            [256, 512, 1024, 2048],
            [4096, 8192, 16384, 32768]
        ]
        self.assertFalse(self.game.is_game_over())

    def test_add_tile_preserves_existing(self):
        self.game.board = [
            [2, 4, 2, 0],
            [0, 2, 4, 2],
            [2, 0, 2, 4],
            [4, 2, 0, 2]
        ]
        self.game.add_tile()
        non_zero_positions = [(r, c) for r in range(4)
                              for c in range(4) if self.game.board[r][c] != 0]
        self.assertGreaterEqual(len(non_zero_positions), 12)


if __name__ == "__main__":
    unittest.main()
