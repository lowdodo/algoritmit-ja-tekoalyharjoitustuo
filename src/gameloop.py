import pygame
from game2048 import Game2048
from ui import UI
from ai import AI2048

class GameLoop:
    def __init__(self, size=4, ai_enabled=False, depth=2):
        self.game = Game2048(size=size)
        self.ui = UI(self.game)
        self.ai_enabled = ai_enabled
        self.depth = depth
        self.running = True

    def apply_move(self, direction):
        if direction == "left":
            new_board = self.game.move_left()
        elif direction == "right":
            new_board = self.game.move_right()
        elif direction == "up":
            new_board = self.game.move_up()
        elif direction == "down":
            new_board = self.game.move_down()
        else:
            return False

        if new_board != self.game.board:
            self.game.board = new_board
            self.game.add_tile()
            return True
        return False

    def run(self):
        clock = pygame.time.Clock()
        self.ui.draw_board(self.ai_enabled)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.ui.ai_button_rect.collidepoint(event.pos):
                        self.ai_enabled = not self.ai_enabled
                        print(f"AI enabled: {self.ai_enabled}")
                elif event.type == pygame.KEYDOWN and not self.ai_enabled:
                    if event.key == pygame.K_LEFT:
                        moved = self.apply_move("left")
                    elif event.key == pygame.K_RIGHT:
                        moved = self.apply_move("right")
                    elif event.key == pygame.K_UP:
                        moved = self.apply_move("up")
                    elif event.key == pygame.K_DOWN:
                        moved = self.apply_move("down")
                    else:
                        moved = False

                    if moved:
                        self.ui.draw_board(self.ai_enabled)

            # AI move
            if self.ai_enabled:
                ai = AI2048(self.game, depth=self.depth)
                direction = ai.best_move(self.game, depth=self.depth)
                if direction:
                    self.apply_move(direction)
                    self.ui.draw_board(self.ai_enabled)

            if self.game.check_win():
                print("You win!")
                self.running = False
            elif self.game.is_game_over():
                print("Game over!")
                self.running = False

            clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    # Regular game:
    loop = GameLoop(ai_enabled=False)
    loop.run()

    # AI autoplay:
    # loop = GameLoop(ai_enabled=True, depth=3)
    # loop.run()
