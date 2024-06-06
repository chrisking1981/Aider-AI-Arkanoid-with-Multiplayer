import pygame
import random

# Power-ups
SHIELD_WIDTH = 100
SHIELD_HEIGHT = 10
SHIELD_DROP_CHANCE = 0.3
ENLARGE_DROP_CHANCE = 0.2

def handle_powerups(bricks, paddle, shield, enlarge, shield_active, enlarge_active, shield_sound, enlarge_sound):
    for brick in bricks[:]:
        if random.random() < SHIELD_DROP_CHANCE:
            shield = pygame.Rect(brick.x + brick.width // 2 - SHIELD_WIDTH // 2, brick.y, SHIELD_WIDTH, SHIELD_HEIGHT)
        elif random.random() < ENLARGE_DROP_CHANCE:
            enlarge = pygame.Rect(brick.x + brick.width // 2 - SHIELD_WIDTH // 2, brick.y, SHIELD_WIDTH, SHIELD_HEIGHT)
    return shield, enlarge

def update_powerups(shield, enlarge, paddle, shield_active, enlarge_active, shield_sound, enlarge_sound, countdown_start_time, SCREEN_HEIGHT):
    if shield:
        shield.y += 5
        if shield.colliderect(paddle):
            shield_active = True
            shield_sound.play()
            shield = None
            countdown_start_time = pygame.time.get_ticks()
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

    return shield, enlarge, shield_active, enlarge_active, countdown_start_time
