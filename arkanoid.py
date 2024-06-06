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
from colors import BLACK, WHITE, BLUE, RED
from powerups import handle_powerups, update_powerups, SHIELD_WIDTH, SHIELD_HEIGHT, SHIELD_DROP_CHANCE, ENLARGE_DROP_CHANCE

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






# Countdown timer
COUNTDOWN_TIME = 30000  # 30 seconds in milliseconds
countdown_start_time = 0

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

shield = None
shield_active = False
shield_activation_time = 0
enlarge = None
enlarge_active = False

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

    ball_dx, ball_dy = move_ball(ball, ball_dx, ball_dy, SCREEN_WIDTH, SCREEN_HEIGHT)

    if ball.colliderect(paddle):
        ball.bottom = paddle.top  # Adjust ball position to be on top of the paddle
        ball_dy = -ball_dy
        paddle_hit_sound.play()
    elif shield_active and ball.colliderect(pygame.Rect(0, SCREEN_HEIGHT - SHIELD_HEIGHT, SCREEN_WIDTH, SHIELD_HEIGHT)):
        ball.bottom = SCREEN_HEIGHT - SHIELD_HEIGHT  # Adjust ball position to be on top of the shield
        ball_dy = -ball_dy
        paddle_hit_sound.play()

    for brick in bricks[:]:
        if ball.colliderect(brick):
            ball_dy = -ball_dy
            bricks.remove(brick)
            brick_hit_sound.play()
            shield, enlarge = handle_powerups(bricks, paddle, shield, enlarge, shield_active, enlarge_active, shield_sound, enlarge_sound)

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
        laser.y -= 15
        if laser.y < 0:
            lasers.remove(laser)
        else:
            for brick in bricks[:]:
                if laser.colliderect(brick):
                    bricks.remove(brick)
                    lasers.remove(laser)
                    brick_hit_sound.play()
                    if random.random() < SHIELD_DROP_CHANCE:
                        shield = pygame.Rect(brick.x + brick.width // 2 - SHIELD_WIDTH // 2, brick.y, SHIELD_WIDTH, SHIELD_HEIGHT)
                    elif random.random() < ENLARGE_DROP_CHANCE:
                        enlarge = pygame.Rect(brick.x + brick.width // 2 - SHIELD_WIDTH // 2, brick.y, SHIELD_WIDTH, SHIELD_HEIGHT)
                    break

    shield, enlarge, shield_active, enlarge_active, countdown_start_time = update_powerups(shield, enlarge, paddle, shield_active, enlarge_active, shield_sound, enlarge_sound, countdown_start_time, SCREEN_HEIGHT)

    if shield_active and pygame.time.get_ticks() - shield_activation_time > 30000:  # 30 seconds
        shield_active = False

    # Update countdown timer
    if shield_active:
        elapsed_time = pygame.time.get_ticks() - countdown_start_time
        remaining_time = max(0, COUNTDOWN_TIME - elapsed_time)
    else:
        remaining_time = 0

    if enlarge_active:
        paddle.width = PADDLE_WIDTH * 2  # Enlarged paddle width
    else:
        paddle.width = PADDLE_WIDTH  # Default paddle width

    SCREEN.fill(BLACK)
    paddle_color = RED if enlarge_active else WHITE
    draw_paddle(SCREEN, paddle, paddle_color, scale_x, scale_y)
    draw_ball(SCREEN, ball, WHITE, scale_x, scale_y)
    for brick in bricks:
        draw_brick(SCREEN, brick, BLUE, scale_x, scale_y)
    font = pygame.font.Font(None, 24)
    
    if shield:
        pygame.draw.rect(SCREEN, BLUE, shield)
        text = font.render("Shield", True, WHITE)
        SCREEN.blit(text, (shield.x, shield.y - 20))
        
    if enlarge:
        pygame.draw.rect(SCREEN, RED, enlarge)
        text = font.render("Enlarge", True, WHITE)
        SCREEN.blit(text, (enlarge.x, enlarge.y - 20))
        
    for laser in lasers:
        pygame.draw.rect(SCREEN, WHITE, laser)

    if shield_active:
        pygame.draw.rect(SCREEN, BLUE, (0, SCREEN_HEIGHT - SHIELD_HEIGHT, SCREEN_WIDTH, SHIELD_HEIGHT))

    # Display countdown timer
    if shield_active:
        minutes = remaining_time // 60000
        seconds = (remaining_time % 60000) // 1000
        timer_text = f"Shield: {minutes:02}:{seconds:02}"
    else:
        timer_text = "Shield: 00:00"

    text = font.render(timer_text, True, WHITE)
    SCREEN.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)
    clock.tick(60)
