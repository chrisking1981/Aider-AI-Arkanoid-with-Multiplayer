import pygame
import sys
import random
import numpy as np

# Initialize Pygame
pygame.init()

# Generate sounds
def generate_sound(frequency, duration, volume=0.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 32767 * volume * np.sin(2 * np.pi * frequency * t)
    sound_array = np.array(wave, dtype=np.int16)
    stereo_sound_array = np.zeros((sound_array.shape[0], 2), dtype=np.int16)
    stereo_sound_array[:, 0] = sound_array  # Left channel
    stereo_sound_array[:, 1] = sound_array  # Right channel
    return pygame.sndarray.make_sound(stereo_sound_array)

paddle_hit_sound = generate_sound(440, 0.1)
brick_hit_sound = generate_sound(880, 0.1)
game_over_sound = generate_sound(220, 0.5)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ASPECT_RATIO = SCREEN_WIDTH / SCREEN_HEIGHT
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Arkanoid")

def maintain_aspect_ratio(event):
    global SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN
    SCREEN_WIDTH = event.w
    SCREEN_HEIGHT = event.h
    if SCREEN_WIDTH / SCREEN_HEIGHT > ASPECT_RATIO:
        SCREEN_WIDTH = int(SCREEN_HEIGHT * ASPECT_RATIO)
    else:
        SCREEN_HEIGHT = int(SCREEN_WIDTH / ASPECT_RATIO)
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Paddle
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_SPEED = 10

# Ball
BALL_SIZE = 10
BALL_SPEED = 5

# Brick
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_ROWS = 5
BRICK_COLUMNS = 10

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

def show_start_screen():
    scale_x = SCREEN_WIDTH / 800
    scale_y = SCREEN_HEIGHT / 600

    SCREEN.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render("Arkanoid", True, WHITE)
    SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 - 50))
    font = pygame.font.Font(None, 36)
    text = font.render("Press SPACE to start", True, WHITE)
    SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 + 50))
    text = font.render("Press Q to quit during the game", True, WHITE)
    SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 + 100))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                    waiting = False

show_start_screen()

clock = pygame.time.Clock()
paddle = create_paddle()
ball, ball_dx, ball_dy = create_ball()
bricks = create_bricks()

while True:
    scale_x = SCREEN_WIDTH / 800
    scale_y = SCREEN_HEIGHT / 600

    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            maintain_aspect_ratio(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                paddle = create_paddle()
                ball, ball_dx, ball_dy = create_ball()
                bricks = create_bricks()
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                paddle = create_paddle()
                ball, ball_dx, ball_dy = create_ball()
                bricks = create_bricks()
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        move_paddle(paddle, -PADDLE_SPEED)
    if keys[pygame.K_RIGHT]:
        move_paddle(paddle, PADDLE_SPEED)

    ball_dx, ball_dy = move_ball(ball, ball_dx, ball_dy)

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
        game_over_sound.play()
        pygame.time.wait(2000)  # Wait for 2 seconds to let the sound play
        show_start_screen()
        paddle = create_paddle()
        ball, ball_dx, ball_dy = create_ball()
        bricks = create_bricks()

    SCREEN.fill(BLACK)
    draw_paddle(paddle, scale_x, scale_y)
    draw_ball(ball, scale_x, scale_y)
    for brick in bricks:
        draw_brick(brick, scale_x, scale_y)
    pygame.display.flip()
    clock.tick(60)
