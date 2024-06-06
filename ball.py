import pygame
import random
def create_ball(screen_width, screen_height, ball_size, ball_speed):
    rect = pygame.Rect(screen_width // 2, screen_height // 2, ball_size, ball_size)
    dx = ball_speed * random.choice((1, -1))
    dy = ball_speed * random.choice((1, -1))
    return rect, dx, dy

def move_ball(ball, dx, dy, screen_width, screen_height):
    ball.x += dx
    ball.y += dy

    if ball.left <= 0 or ball.right >= screen_width:
        dx = -dx
    if ball.top <= 0:
        dy = -dy

    if ball.bottom >= screen_height:
        dy = -dy

    return dx, dy

def draw_ball(screen, ball, color, scale_x, scale_y):
    scaled_ball = pygame.Rect(ball.x * scale_x, ball.y * scale_y, ball.width * scale_x, ball.height * scale_y)
    pygame.draw.ellipse(screen, color, scaled_ball)
