import pygame
import sys
from colors import BLACK, WHITE

def show_start_screen(SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT):
    scale_x = SCREEN_WIDTH / 800
    scale_y = SCREEN_HEIGHT / 600

    SCREEN.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render("Arkanoid", True, WHITE)
    SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 - 50))
    font = pygame.font.Font(None, 36)
    text = font.render("Press S to start", True, WHITE)
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
                if event.key == pygame.K_s:
                    waiting = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                    waiting = False
