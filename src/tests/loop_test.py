import unittest
from gameloop import GameLoop
import pygame


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

    def test_apply_move_valid_direction(self):
        self.game_loop.game.board = [
            [2, 0, 2, 4],
            [4, 4, 0, 0],
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ]
        moved = self.game_loop.apply_move("left")
        self.assertTrue(moved)
        expected = [
            [4, 4, 0, 0],
            [8, 0, 0, 0],
            [4, 4, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertEqual(self.game_loop.game.board, expected)

    def test_toggle_ai(self):
        initial_state = self.game_loop.ai_enabled
        self.game_loop.toggle_ai()
        self.assertNotEqual(self.game_loop.ai_enabled, initial_state)
        if self.game_loop.ai_enabled:
            self.assertIsNotNone(self.game_loop.ai)
        else:
            self.assertIsNone(self.game_loop.ai)   
    
    def test_toggle_ai_multiple_times(self):
        for _ in range(5):
            current_state = self.game_loop.ai_enabled
            self.game_loop.toggle_ai()
            self.assertNotEqual(self.game_loop.ai_enabled, current_state)
            if self.game_loop.ai_enabled:
                self.assertIsNotNone(self.game_loop.ai)
            else:
                self.assertIsNone(self.game_loop.ai)

    def test_run_loop_key_event_no_ai(self):
        self.game_loop.ai_enabled = False
        self.game_loop.ai = None
        self.game_loop.game.board = [
            [2, 0, 2, 4],
            [4, 4, 0, 0],
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ]

        pygame_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)
        pygame.event.post(pygame_event)

        pygame.event.post(pygame.event.Event(pygame.QUIT))

        self.game_loop.run()

        expected_board = [
            [4, 4, 0, 0],
            [8, 0, 0, 0],
            [4, 4, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertEqual(self.game_loop.game.board, expected_board) 