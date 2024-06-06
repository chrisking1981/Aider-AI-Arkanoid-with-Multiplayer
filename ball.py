import pygame
import random
from arkanoid import SCREEN, WHITE, BALL_SIZE, BALL_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT

def create_ball():
    rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_SIZE, BALL_SIZE)
    dx = BALL_SPEED * random.choice((1, -1))
    dy = BALL_SPEED * random.choice((1, -1))
    return rect, dx, dy

def move_ball(ball, dx, dy):
    ball.x += dx
    ball.y += dy

    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        dx = -dx
    if ball.top <= 0:
        dy = -dy

    return dx, dy

def draw_ball(ball, scale_x, scale_y):
    scaled_ball = pygame.Rect(ball.x * scale_x, ball.y * scale_y, ball.width * scale_x, ball.height * scale_y)
    pygame.draw.ellipse(SCREEN, WHITE, scaled_ball)
