import pygame

def create_paddle(screen_width, screen_height, paddle_width, paddle_height):
    return pygame.Rect((screen_width // 2) - (paddle_width // 2), screen_height - 30, paddle_width, paddle_height)

def move_paddle(paddle, dx, screen_width, paddle_width):
    paddle.x += dx
    if paddle.x < 0:
        paddle.x = 0
    if paddle.x > screen_width - paddle_width:
        paddle.x = screen_width - paddle_width

def draw_paddle(screen, paddle, color, scale_x, scale_y):
    scaled_paddle = pygame.Rect(paddle.x * scale_x, paddle.y * scale_y, paddle.width * scale_x, paddle.height * scale_y)
    pygame.draw.rect(screen, color, scaled_paddle)
