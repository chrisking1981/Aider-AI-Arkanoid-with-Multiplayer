import pygame
import sys
import random
import numpy as np

# Initialize Pygame
pygame.init()

from sound import paddle_hit_sound, brick_hit_sound, game_over_sound, laser_sound, shield_sound, enlarge_sound
from start_screen import show_start_screen
from paddle import create_paddle, move_paddle, draw_paddle
from ball import create_ball, move_ball, draw_ball
from brick import create_bricks, draw_brick
from colors import BLACK, WHITE, BLUE, GREEN

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

def shoot_laser(paddle, lasers, last_shot_time, cooldown):
    current_time = pygame.time.get_ticks()
    if current_time - last_shot_time >= cooldown:
        laser = pygame.Rect(paddle.x + paddle.width // 2 - 2, paddle.y - 20, 4, 20)
        lasers.append(laser)
        laser_sound.play()
        return current_time
    return last_shot_time
    laser = pygame.Rect(paddle.x + paddle.width // 2 - 2, paddle.y - 20, 4, 20)
    lasers.append(laser)

lasers = []

lasers = []
last_shot_time = 0
cooldown = 125  # Cooldown period in milliseconds

# Power-ups
SHIELD_WIDTH = 100
SHIELD_HEIGHT = 10
SHIELD_DROP_CHANCE = 0.3
ENLARGE_DROP_CHANCE = 0.2
shield = None
shield_active = False
enlarge = None
enlarge_active = False
SHIELD_WIDTH = 100
SHIELD_HEIGHT = 10
SHIELD_DROP_CHANCE = 0.3
shield = None
shield_active = False

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
    elif keys[pygame.K_SPACE]:
        last_shot_time = shoot_laser(paddle, lasers, last_shot_time, cooldown)

    ball_dx, ball_dy = move_ball(ball, ball_dx, ball_dy, SCREEN_WIDTH)

    if ball.colliderect(paddle):
        ball_dy = -ball_dy
        paddle_hit_sound.play()
    elif shield_active and ball.colliderect(pygame.Rect(0, SCREEN_HEIGHT - SHIELD_HEIGHT, SCREEN_WIDTH, SHIELD_HEIGHT)):
        ball_dy = -ball_dy
        paddle_hit_sound.play()

    for brick in bricks[:]:
        if ball.colliderect(brick):
            ball_dy = -ball_dy
            bricks.remove(brick)
            brick_hit_sound.play()
            if random.random() < SHIELD_DROP_CHANCE:
                shield = pygame.Rect(brick.x + brick.width // 2 - SHIELD_WIDTH // 2, brick.y, SHIELD_WIDTH, SHIELD_HEIGHT)
            elif random.random() < ENLARGE_DROP_CHANCE:
                enlarge = pygame.Rect(brick.x + brick.width // 2 - SHIELD_WIDTH // 2, brick.y, SHIELD_WIDTH, SHIELD_HEIGHT)

    if ball.colliderect(paddle) or (shield_active and ball.colliderect(pygame.Rect(0, SCREEN_HEIGHT - SHIELD_HEIGHT, SCREEN_WIDTH, SHIELD_HEIGHT))):
        ball_dy = -ball_dy
        paddle_hit_sound.play()

    if ball.bottom >= SCREEN_HEIGHT:
        game_over_sound.play()
        pygame.time.wait(2000)  # Wait for 2 seconds to let the sound play
        show_start_screen(SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT)
        paddle = create_paddle(SCREEN_WIDTH, SCREEN_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT)
        ball, ball_dx, ball_dy = create_ball(SCREEN_WIDTH, SCREEN_HEIGHT, BALL_SIZE, BALL_SPEED)
        bricks = create_bricks()

    for laser in lasers[:]:
        laser.y -= 10
        if laser.y < 0:
            lasers.remove(laser)
        else:
            for brick in bricks[:]:
                if laser.colliderect(brick):
                    bricks.remove(brick)
                    lasers.remove(laser)
                    brick_hit_sound.play()
                    break

    if shield:
        shield.y += 5
        if shield.colliderect(paddle):
            shield_active = True
            shield_sound.play()
            shield = None
        elif shield.y > SCREEN_HEIGHT:
            shield = None

    if enlarge:
        enlarge.y += 5
        if enlarge.colliderect(paddle):
            enlarge_active = True
            enlarge_sound.play()
            enlarge = None
        elif enlarge.y > SCREEN_HEIGHT:
            enlarge = None

    if enlarge_active:
        PADDLE_WIDTH = 150  # Enlarged paddle width
    else:
        PADDLE_WIDTH = 100  # Default paddle width

    SCREEN.fill(BLACK)
    draw_paddle(SCREEN, paddle, WHITE, scale_x, scale_y)
    draw_ball(SCREEN, ball, WHITE, scale_x, scale_y)
    for brick in bricks:
        draw_brick(SCREEN, brick, BLUE, scale_x, scale_y)
    font = pygame.font.Font(None, 24)
    
    if shield:
        pygame.draw.rect(SCREEN, BLUE, shield)
        text = font.render("Shield", True, WHITE)
        SCREEN.blit(text, (shield.x, shield.y - 20))
        
    if enlarge:
        pygame.draw.rect(SCREEN, GREEN, enlarge)
        text = font.render("Enlarge", True, WHITE)
        SCREEN.blit(text, (enlarge.x, enlarge.y - 20))
        
    for laser in lasers:
        pygame.draw.rect(SCREEN, WHITE, laser)

    if shield_active:
        pygame.draw.rect(SCREEN, BLUE, (0, SCREEN_HEIGHT - SHIELD_HEIGHT, SCREEN_WIDTH, SHIELD_HEIGHT))

    pygame.display.flip()
    clock.tick(60)
    clock.tick(60)
