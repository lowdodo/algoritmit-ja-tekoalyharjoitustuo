import unittest
from game2048 import Game2048


class TestGame2048(unittest.TestCase):
    def setUp(self):
        return super().setUp()

    # movement tests:

    def test_move_left(self):
        game = Game2048()
        game.board = [
            [2, 0, 2, 4],
            [4, 4, 0, 0],
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ]
        expected_board = [
            [4, 4, 0, 0],
            [8, 0, 0, 0],
            [4, 4, 0, 0],
            [0, 0, 0, 0]
        ]
        new_board = game.move_left()
        self.assertEqual(new_board, expected_board)

    def test_move_right(self):
        game = Game2048()
        game.board = [
            [2, 0, 2, 4],
            [4, 4, 0, 0],
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ]
        expected_board = [
            [0, 0, 4, 4],
            [0, 0, 0, 8],
            [0, 0, 4, 4],
            [0, 0, 0, 0]
        ]
        new_board = game.move_right()
        self.assertEqual(new_board, expected_board)

    def test_move_up(self):
        game = Game2048()
        game.board = [
            [2, 0, 2, 4],
            [4, 4, 0, 0],
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ]
        expected_board = [
            [2, 4, 4, 4],
            [4, 2, 0, 2],
            [2, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        new_board = game.move_up()
        self.assertEqual(new_board, expected_board)

    def test_move_down(self):
        game = Game2048()
        game.board = [
            [2, 0, 2, 4],
            [4, 4, 0, 0],
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ]
        expected_board = [
            [0, 0, 0, 0],
            [2, 0, 0, 0],
            [4, 4, 0, 4],
            [2, 2, 4, 2]
        ]
        new_board = game.move_down()
        self.assertEqual(new_board, expected_board)

    # board tests:
    def test_beginning_tiles(self):
        game = Game2048()
        non_empty_tiles = sum(
            1 for row in game.board for tile in row if tile != 0)
        self.assertEqual(
            non_empty_tiles, 2, "There should be exactly two tiles at the start of the game.")
        self.assertTrue(all(tile in (0, 2, 4) for row in game.board for tile in row),
                        "Tiles should be either 0, 2, or 4.")
        self.assertTrue(any(tile == 2 for row in game.board for tile in row),
                        "At least one tile should be a 2.")

    def test_add_tile(self):
        game = Game2048()
        game.board = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 0],
            [4, 2, 4, 2]
        ]
        game.add_tile()
        non_empty_tiles = sum(
            1 for row in game.board for tile in row if tile != 0)
        self.assertEqual(non_empty_tiles, 16,
                         "There should be exactly one new tile added.")
        self.assertTrue(any(tile == 2 or tile == 4 for row in game.board for tile in row if tile != 0),
                        "The new tile should be either a 2 or a 4.")
        
    def test_game_over(self):
        game = Game2048()
        game.board = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2]
        ]
        self.assertTrue(game.is_game_over(),
                        "The game should be over when no moves are possible.")
        
    def test_not_game_over(self):
        game = Game2048()
        game.board = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 0],
            [4, 2, 4, 2]
        ]
        self.assertFalse(game.is_game_over(),
                         "The game should not be over when moves are still possible.") 

    def test_game_over_no_empty_but_merge_possible_row(self):
        game = Game2048()
        game.board = [
            [2, 2, 4, 8],
            [16, 32, 64, 128],
            [256, 512, 1024, 2048],
            [4096, 8192, 16384, 32768]
        ]
        self.assertFalse(game.is_game_over(), "Game should not be over if a horizontal merge is possible")

    def test_game_over_no_empty_but_merge_possible_column(self):
        game = Game2048()
        game.board = [
            [2, 4, 8, 16],
            [2, 32, 64, 128],
            [256, 512, 1024, 2048],
            [4096, 8192, 16384, 32768]
        ]
        self.assertFalse(game.is_game_over(), "Game should not be over if a vertical merge is possible")

    def test_game_over_full_no_merge(self):
        game = Game2048()
        game.board = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2]
        ]
        self.assertTrue(game.is_game_over(), "Game should be over if board is full and no merges possible")

    def test_check_win_true(self):
        game = Game2048()
        game.board = [
            [2, 4, 2, 4],
            [4, 2048, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2]
        ]
        self.assertTrue(game.check_win(), "check_win should return True if 2048 tile exists")

    def test_check_win_false(self):
        game = Game2048()
        game.board = [
            [2, 4, 2, 4],
            [4, 8, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2]
        ]
        self.assertFalse(game.check_win(), "check_win should return False if no 2048 tile exists")
