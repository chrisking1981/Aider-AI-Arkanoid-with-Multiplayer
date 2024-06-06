import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arkanoid")

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

class Paddle:
    def __init__(self):
        self.rect = pygame.Rect((SCREEN_WIDTH // 2) - (PADDLE_WIDTH // 2), SCREEN_HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, dx):
        self.rect.x += dx
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - PADDLE_WIDTH:
            self.rect.x = SCREEN_WIDTH - PADDLE_WIDTH

    def draw(self):
        pygame.draw.rect(SCREEN, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_SIZE, BALL_SIZE)
        self.dx = BALL_SPEED * random.choice((1, -1))
        self.dy = BALL_SPEED * random.choice((1, -1))

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.dx = -self.dx
        if self.rect.top <= 0:
            self.dy = -self.dy

    def draw(self):
        pygame.draw.ellipse(SCREEN, WHITE, self.rect)

class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)

    def draw(self):
        pygame.draw.rect(SCREEN, BLUE, self.rect)

def create_bricks():
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLUMNS):
            brick = Brick(col * (BRICK_WIDTH + 10) + 35, row * (BRICK_HEIGHT + 10) + 35)
            bricks.append(brick)
    return bricks

def main():
    clock = pygame.time.Clock()
    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move(-PADDLE_SPEED)
        if keys[pygame.K_RIGHT]:
            paddle.move(PADDLE_SPEED)

        ball.move()

        if ball.rect.colliderect(paddle.rect):
            ball.dy = -ball.dy

        for brick in bricks[:]:
            if ball.rect.colliderect(brick.rect):
                ball.dy = -ball.dy
                bricks.remove(brick)

        if ball.rect.bottom >= SCREEN_HEIGHT:
            pygame.quit()
            sys.exit()

        SCREEN.fill(BLACK)
        paddle.draw()
        ball.draw()
        for brick in bricks:
            brick.draw()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
