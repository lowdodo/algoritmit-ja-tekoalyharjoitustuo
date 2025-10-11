import unittest
from gameloop import GameLoop
from ai import AI2048
import pygame
from unittest.mock import MagicMock


class TestGameLoop(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize pygame once for all tests (safe headless setup)."""
        pygame.init()
        pygame.display.set_mode((1, 1))
        pygame.font.init()

    @classmethod
    def tearDownClass(cls):
        """Quit pygame cleanly."""
        pygame.quit()

    def setUp(self):
        """Create a fresh game loop for each test."""
        self.game_loop = GameLoop()
        self.ai = AI2048(self.game_loop.game, depth=1)

        # Disable random tile addition for deterministic results
        self.game_loop.game.add_tile = lambda: None

        # ✅ Mock out all Pygame-dependent UI functions
        self.game_loop.ui.draw_board = MagicMock()
        self.game_loop.ui.draw_tile = MagicMock()

    def test_apply_move_invalid_direction(self):
        """Invalid directions should not modify the board."""
        self.game_loop.game.board = [
            [2, 0, 2, 4],
            [4, 4, 0, 0],
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ]
        moved = self.game_loop.apply_move("invalid_direction")
        self.assertFalse(moved)
        expected = [
            [2, 0, 2, 4],
            [4, 4, 0, 0],
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ]
        self.assertEqual(self.game_loop.game.board, expected)

    def test_apply_move_valid_direction(self):
        """A valid move (left) should merge and slide tiles correctly."""
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
        """Toggling AI should enable and disable AI alternately."""
        initial_state = self.game_loop.ai_enabled
        self.game_loop.toggle_ai()
        self.assertNotEqual(self.game_loop.ai_enabled, initial_state)
        if self.game_loop.ai_enabled:
            self.assertIsNotNone(self.game_loop.ai)
        else:
            self.assertIsNone(self.game_loop.ai)

    def test_toggle_ai_multiple_times(self):
        """Repeated toggles should alternate the AI state each time."""
        for _ in range(5):
            current_state = self.game_loop.ai_enabled
            self.game_loop.toggle_ai()
            self.assertNotEqual(self.game_loop.ai_enabled, current_state)
            if self.game_loop.ai_enabled:
                self.assertIsNotNone(self.game_loop.ai)
            else:
                self.assertIsNone(self.game_loop.ai)

    def test_run_loop_key_event_no_ai(self):
        """Pressing LEFT key without AI should apply move and exit."""
        self.game_loop.ai_enabled = False
        self.game_loop.ai = None
        self.game_loop.game.board = [
            [2, 0, 2, 4],
            [4, 4, 0, 0],
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ]

        pygame.event.post(pygame.event.Event(
            pygame.KEYDOWN, key=pygame.K_LEFT))
        pygame.event.post(pygame.event.Event(pygame.QUIT))

        self.game_loop.run()

        expected_board = [
            [4, 4, 0, 0],
            [8, 0, 0, 0],
            [4, 4, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertEqual(self.game_loop.game.board, expected_board)

    def test_run_loop_with_ai_enabled(self):
        """Simulate one loop iteration with AI making a move."""
        self.game_loop.ai_enabled = True
        self.game_loop.ai = self.ai
        self.game_loop.ai.best_move = lambda: "left"
        self.game_loop.game.is_game_over = lambda: True
        self.game_loop.apply_move = MagicMock(return_value=True)

        pygame.event.post(pygame.event.Event(pygame.QUIT))
        self.game_loop.run()

        self.assertTrue(self.game_loop.ai_enabled)
        self.game_loop.apply_move.assert_called_once_with("left")

    def _simulate_run_with_key(self, key):
        """Helper to simulate pressing a direction key once."""
        self.game_loop.ai_enabled = False
        self.game_loop.game.add_tile = lambda: None

        self.game_loop.game.board = [
            [2, 0, 2, 4],
            [4, 4, 0, 0],
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ]

        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=key))
        pygame.event.post(pygame.event.Event(pygame.QUIT))

        self.board_redrawn = False
        self.game_loop.ui.draw_board = lambda ai_enabled=False: setattr(
            self, "board_redrawn", True)
        self.game_loop.run()
        return self.game_loop.game.board

    def test_run_loop_key_right(self):
        """Pressing RIGHT key should slide all tiles right."""
        final_board = self._simulate_run_with_key(pygame.K_RIGHT)
        expected = [
            [0, 0, 4, 4],
            [0, 0, 0, 8],
            [0, 0, 4, 4],
            [0, 0, 0, 0]
        ]
        self.assertEqual(final_board, expected)
        self.assertTrue(self.board_redrawn)

    def test_run_loop_key_up(self):
        """Pressing UP key should move tiles upward."""
        final_board = self._simulate_run_with_key(pygame.K_UP)
        expected = [
            [2, 4, 4, 4],
            [4, 2, 0, 2],
            [2, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertEqual(final_board, expected)
        self.assertTrue(self.board_redrawn)

    def test_run_loop_key_down(self):
        """Pressing DOWN key should move tiles downward."""
        final_board = self._simulate_run_with_key(pygame.K_DOWN)
        expected = [
            [0, 0, 0, 0],
            [2, 0, 0, 0],
            [4, 4, 0, 4],
            [2, 2, 4, 2]
        ]
        self.assertEqual(final_board, expected)
        self.assertTrue(self.board_redrawn)

    def test_button_click_toggles_ai(self):
        """Clicking the AI button should toggle AI state."""
        self.game_loop.ui.ai_button_rect = pygame.Rect(0, 0, 100, 50)
        initial_state = self.game_loop.ai_enabled

        pygame.event.post(pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, pos=(10, 10)))
        pygame.event.post(pygame.event.Event(pygame.QUIT))

        self.game_loop.run()
        self.assertNotEqual(self.game_loop.ai_enabled, initial_state)
        self.game_loop.ui.draw_board.assert_called()


if __name__ == "__main__":
    unittest.main()
