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
from colors import BLACK, WHITE, BLUE, RED, GREEN
from powerups import handle_powerups, update_powerups, handle_shield, update_shield, handle_enlarge, update_enlarge, shoot_laser, update_lasers, SHIELD_WIDTH, SHIELD_HEIGHT, LASER_COOLDOWN, LASER_SIZE

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

font = pygame.font.Font(None, 24)
show_start_screen(SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT)

clock = pygame.time.Clock()
paddle = create_paddle(SCREEN_WIDTH, SCREEN_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT)
ball, ball_dx, ball_dy = create_ball(SCREEN_WIDTH, SCREEN_HEIGHT, BALL_SIZE, BALL_SPEED, paddle)
ball_stuck = True
ball_stuck = True
bricks = create_bricks()


laser = None
lasers = []
laser_active = False

lasers = []
last_shot_time = 0

shield = None
shield_active = False
shield_activation_time = 0
enlarge = None
enlarge_active = False
laser = None

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
    if ball_stuck:
        ball.x = paddle.x + paddle.width // 2 - BALL_SIZE // 2
        ball.y = paddle.y - BALL_SIZE
        if keys[pygame.K_s] or keys[pygame.K_SPACE]:
            ball_stuck = False
            ball_dx, ball_dy = BALL_SPEED * random.choice((1, -1)), -BALL_SPEED  # Launch the ball
    else:
        ball_dx, ball_dy = move_ball(ball, ball_dx, ball_dy, SCREEN_WIDTH, SCREEN_HEIGHT)
    if laser_active and keys[pygame.K_s]:
        last_shot_time = shoot_laser(paddle, lasers, last_shot_time, LASER_COOLDOWN, laser_sound)

    if not ball_stuck:
        ball_dx, ball_dy = move_ball(ball, ball_dx, ball_dy, SCREEN_WIDTH, SCREEN_HEIGHT)

    if not ball_stuck and ball.colliderect(paddle):
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
            shield, enlarge, laser = handle_powerups(brick, paddle, shield, enlarge, laser, shield_active, enlarge_active, laser_active, shield_sound, enlarge_sound, laser_sound)
            break

    if not ball_stuck and ball.bottom >= SCREEN_HEIGHT:
        game_over_sound.play()
        pygame.time.wait(2000)  # Wait for 2 seconds to let the sound play
        show_start_screen(SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT)
        paddle = create_paddle(SCREEN_WIDTH, SCREEN_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT)
        ball, ball_dx, ball_dy = create_ball(SCREEN_WIDTH, SCREEN_HEIGHT, BALL_SIZE, BALL_SPEED, paddle)
        bricks = create_bricks()

    lasers, shield, enlarge, laser = update_lasers(lasers, bricks, brick_hit_sound, paddle, shield, enlarge, laser, shield_active, enlarge_active, laser_active, shield_sound, enlarge_sound, laser_sound)

    shield, enlarge, laser, shield_active, enlarge_active, laser_active, countdown_start_time = update_powerups(shield, enlarge, laser, paddle, shield_active, enlarge_active, laser_active, shield_sound, enlarge_sound, laser_sound, countdown_start_time, SCREEN_HEIGHT)
    shield, shield_active, countdown_start_time = update_shield(shield, paddle, shield_active, shield_sound, countdown_start_time, SCREEN_HEIGHT)
    enlarge, enlarge_active = update_enlarge(enlarge, paddle, enlarge_active, enlarge_sound, SCREEN_HEIGHT)

    if shield_active and pygame.time.get_ticks() - shield_activation_time > 30000:  # 30 seconds
        shield_active = False

    # Update countdown timer
    if laser:
        pygame.draw.rect(SCREEN, RED, laser)
        text = font.render("L", True, WHITE)
        SCREEN.blit(text, (laser.x + 5, laser.y + 5))
        text = font.render("Laser", True, WHITE)
        SCREEN.blit(text, (laser.x, laser.y - 20))

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
    paddle_color = BLUE if enlarge_active else WHITE
    draw_paddle(SCREEN, paddle, paddle_color, scale_x, scale_y)
    draw_ball(SCREEN, ball, WHITE, scale_x, scale_y)
    for brick in bricks:
        draw_brick(SCREEN, brick, BLUE, scale_x, scale_y)
    
    for laser in lasers:
        pygame.draw.rect(SCREEN, RED, laser)
        
    if shield:
        pygame.draw.rect(SCREEN, GREEN, shield)
        text = font.render("S", True, WHITE)
        SCREEN.blit(text, (shield.x + 5, shield.y + 5))

    if enlarge:
        pygame.draw.rect(SCREEN, BLUE, enlarge)
        text = font.render("E", True, WHITE)
        SCREEN.blit(text, (enlarge.x + 5, enlarge.y + 5))

    if laser:
        pygame.draw.rect(SCREEN, RED, laser)

    if shield_active:
        pygame.draw.rect(SCREEN, GREEN, (0, SCREEN_HEIGHT - SHIELD_HEIGHT, SCREEN_WIDTH, SHIELD_HEIGHT))

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
