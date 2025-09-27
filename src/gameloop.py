import pygame
from game2048 import Game2048
from ui import UI
from ai import AI2048


class GameLoop:
    '''Class to manage the game loop, user input, and AI integration.
    
    Attributes:
        game (Game2048): The current game state.
        ui (UI): The user interface for rendering the game.
        ai_enabled (bool): Flag to indicate if AI is enabled.
        depth (int): The depth for the AI's expectiminimax algorithm.
        '''
    def __init__(self, size=4, ai_enabled=False, depth=2):
        self.game = Game2048(size=size)
        self.ui = UI(self.game)
        self.ai_enabled = ai_enabled
        self.depth = depth
        self.running = True

        self.ai = AI2048(
            self.game, depth=self.depth) if self.ai_enabled else None

    def apply_move(self, direction):
        '''Apply a move in the given direction and return if the board changed.'''
        _, moved = self.game.move(direction)
        return moved

    def toggle_ai(self):
        '''Determine if the AI is on or off.'''
        self.ai_enabled = not self.ai_enabled
        if self.ai_enabled:
            self.ai = AI2048(self.game, depth=self.depth)
        else:
            self.ai = None
        print(f"AI enabled: {self.ai_enabled}")

    def run(self):
        '''Main game loop handling events, AI moves, and rendering.'''
        clock = pygame.time.Clock()
        self.ui.draw_board(self.ai_enabled)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.ui.ai_button_rect.collidepoint(event.pos):
                        self.toggle_ai()
                        self.ui.draw_board(self.ai_enabled)
                elif event.type == pygame.KEYDOWN and not self.ai_enabled:
                    moved = False
                    if event.key == pygame.K_LEFT:
                        moved = self.apply_move("left")
                    elif event.key == pygame.K_RIGHT:
                        moved = self.apply_move("right")
                    elif event.key == pygame.K_UP:
                        moved = self.apply_move("up")
                    elif event.key == pygame.K_DOWN:
                        moved = self.apply_move("down")

                    if moved:
                        self.ui.draw_board(self.ai_enabled)

            if self.ai_enabled and self.ai:
                direction = self.ai.best_move()
                print("AI chose:", direction)
                if direction:
                    moved = self.apply_move(direction)
                    if moved:
                        self.ui.draw_board(self.ai_enabled)

            if self.game.is_game_over():
                self.ui.draw_board(self.ai_enabled)
                pygame.time.wait(1200)
                print("Game over!")
                self.running = False

            clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    # Regular game
    loop = GameLoop(ai_enabled=False)
    loop.run()

    # AI autoplay
    # loop = GameLoop(ai_enabled=True, depth=3)
    # loop.run()
