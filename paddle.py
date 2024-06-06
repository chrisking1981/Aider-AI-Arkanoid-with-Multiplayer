import pygame
from arkanoid import SCREEN, WHITE, PADDLE_WIDTH, PADDLE_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT

def create_paddle():
    return pygame.Rect((SCREEN_WIDTH // 2) - (PADDLE_WIDTH // 2), SCREEN_HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)

def move_paddle(paddle, dx):
    paddle.x += dx
    if paddle.x < 0:
        paddle.x = 0
    if paddle.x > SCREEN_WIDTH - PADDLE_WIDTH:
        paddle.x = SCREEN_WIDTH - PADDLE_WIDTH

def draw_paddle(paddle, scale_x, scale_y):
    scaled_paddle = pygame.Rect(paddle.x * scale_x, paddle.y * scale_y, paddle.width * scale_x, paddle.height * scale_y)
    pygame.draw.rect(SCREEN, WHITE, scaled_paddle)
