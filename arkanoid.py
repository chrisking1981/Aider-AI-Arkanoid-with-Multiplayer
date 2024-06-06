import pygame
import sys
import random
import numpy as np

# Initialize Pygame
pygame.init()

from sound import paddle_hit_sound, brick_hit_sound, game_over_sound
from start_screen import show_start_screen
from paddle import create_paddle, move_paddle, draw_paddle
from ball import create_ball, move_ball, draw_ball
from brick import create_bricks, draw_brick
from colors import BLACK, WHITE, BLUE

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ASPECT_RATIO = SCREEN_WIDTH / SCREEN_HEIGHT
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Arkanoid")

from screen import maintain_aspect_ratio


# Paddle
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_SPEED = 15

# Ball
BALL_SIZE = 10
BALL_SPEED = 8






show_start_screen(SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT)

clock = pygame.time.Clock()
paddle = create_paddle(SCREEN_WIDTH, SCREEN_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT)
ball, ball_dx, ball_dy = create_ball(SCREEN_WIDTH, SCREEN_HEIGHT, BALL_SIZE, BALL_SPEED)
bricks = create_bricks()

while True:
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            maintain_aspect_ratio(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    scale_x = SCREEN_WIDTH / 800
    scale_y = SCREEN_HEIGHT / 600

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        move_paddle(paddle, -PADDLE_SPEED, SCREEN_WIDTH, PADDLE_WIDTH)
    if keys[pygame.K_RIGHT]:
        move_paddle(paddle, PADDLE_SPEED, SCREEN_WIDTH, PADDLE_WIDTH)

    ball_dx, ball_dy = move_ball(ball, ball_dx, ball_dy, SCREEN_WIDTH)

    if ball.colliderect(paddle):
        ball_dy = -ball_dy
        paddle_hit_sound.play()

    for brick in bricks[:]:
        if ball.colliderect(brick):
            ball_dy = -ball_dy
            bricks.remove(brick)
            brick_hit_sound.play()

    if ball.bottom >= SCREEN_HEIGHT:
        game_over_sound.play()
        pygame.time.wait(2000)  # Wait for 2 seconds to let the sound play
        show_start_screen(SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT)
        paddle = create_paddle(SCREEN_WIDTH, SCREEN_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT)
        ball, ball_dx, ball_dy = create_ball(SCREEN_WIDTH, SCREEN_HEIGHT, BALL_SIZE, BALL_SPEED)
        bricks = create_bricks()

    SCREEN.fill(BLACK)
    draw_paddle(SCREEN, paddle, WHITE, scale_x, scale_y)
    draw_ball(SCREEN, ball, WHITE, scale_x, scale_y)
    for brick in bricks:
        draw_brick(SCREEN, brick, BLUE, scale_x, scale_y)
    pygame.display.flip()
    clock.tick(60)
    clock.tick(60)
