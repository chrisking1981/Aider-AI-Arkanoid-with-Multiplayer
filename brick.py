import pygame
from colors import BLUE

BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_ROWS = 5
BRICK_COLUMNS = 10

class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)

    @staticmethod
    def create_bricks():
        bricks = []
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLUMNS):
                brick = Brick(col * (BRICK_WIDTH + 10) + 35, row * (BRICK_HEIGHT + 10) + 35)
                bricks.append(brick)
        return bricks

    @staticmethod
    def draw(screen, brick, color, scale_x, scale_y):
        scaled_brick = pygame.Rect(brick.rect.x * scale_x, brick.rect.y * scale_y, brick.rect.width * scale_x, brick.rect.height * scale_y)
        pygame.draw.rect(screen, color, scaled_brick)
