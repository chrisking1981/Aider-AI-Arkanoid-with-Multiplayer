import pygame

BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_ROWS = 5
BRICK_COLUMNS = 10

def create_brick(x, y):
    return pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)

def draw_brick(brick, scale_x, scale_y):
    scaled_brick = pygame.Rect(brick.x * scale_x, brick.y * scale_y, brick.width * scale_x, brick.height * scale_y)
    pygame.draw.rect(SCREEN, BLUE, scaled_brick)

def create_bricks():
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLUMNS):
            brick = create_brick(col * (BRICK_WIDTH + 10) + 35, row * (BRICK_HEIGHT + 10) + 35)
            bricks.append(brick)
    return bricks
