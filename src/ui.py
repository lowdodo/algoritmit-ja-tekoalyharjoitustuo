import pygame
from game2048 import Game2048

pygame.init()

TILE_SIZE = 100
GAP_SIZE = 10
MARGIN = 20
BACKGROUND_COLOR = (230, 220, 230)
EMPTY_COLOR = (245, 240, 245)

TILE_COLORS = {
    2: (235, 225, 245),
    4: (220, 200, 235),
    8: (200, 175, 225),
    16: (180, 150, 215),
    32: (160, 125, 205),
    64: (140, 100, 195),
    128: (120, 80, 185),
    256: (100, 60, 165),
    512: (80, 40, 145),
    1024: (60, 25, 120),
    2048: (40, 10, 90)
}

FONT = pygame.font.SysFont("comicsansms", 40)
FONT_COLOR_LIGHT = (250, 245, 255)
FONT_COLOR_DARK = (60, 40, 80) 

class UI:
    def __init__(self, game: Game2048):
        self.game = game
        self.screen_size = game.size * TILE_SIZE + (game.size + 1) * GAP_SIZE + 2 * MARGIN
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        pygame.display.set_caption("2048")

    def draw_tile(self, value, x, y):
        color = TILE_COLORS.get(value, EMPTY_COLOR) if value != 0 else EMPTY_COLOR
        pygame.draw.rect(self.screen, color, (x, y, TILE_SIZE, TILE_SIZE))

        if value != 0:
            text_color = FONT_COLOR_DARK if value <= 8 else FONT_COLOR_LIGHT
            text = FONT.render(str(value), True, text_color)
            text_rect = text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
            self.screen.blit(text, text_rect)

    def draw_board(self):
        self.screen.fill(BACKGROUND_COLOR)
        for row in range(self.game.size):
            for col in range(self.game.size):
                x = MARGIN + col * (TILE_SIZE + GAP_SIZE)
                y = MARGIN + row * (TILE_SIZE + GAP_SIZE)
                self.draw_tile(self.game.board[row][col], x, y)
        pygame.display.flip()
