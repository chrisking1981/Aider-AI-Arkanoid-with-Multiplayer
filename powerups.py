import pygame
import random

# Power-ups
SHIELD_WIDTH = 100
SHIELD_HEIGHT = 10
SHIELD_DROP_CHANCE = 0.3
ENLARGE_DROP_CHANCE = 0.2
LASER_DROP_CHANCE = 0.1

def handle_powerups(bricks, paddle, shield, enlarge, laser, shield_active, enlarge_active, laser_active, shield_sound, enlarge_sound, laser_sound):
    for brick in bricks[:]:
        drop_chance = random.random()
        if drop_chance < SHIELD_DROP_CHANCE:
            shield = pygame.Rect(brick.x + brick.width // 2 - SHIELD_WIDTH // 2, brick.y, SHIELD_WIDTH, SHIELD_HEIGHT)
        elif drop_chance < SHIELD_DROP_CHANCE + ENLARGE_DROP_CHANCE:
            enlarge = pygame.Rect(brick.x + brick.width // 2 - SHIELD_WIDTH // 2, brick.y, SHIELD_WIDTH, SHIELD_HEIGHT)
        elif drop_chance < SHIELD_DROP_CHANCE + ENLARGE_DROP_CHANCE + LASER_DROP_CHANCE:
            laser = pygame.Rect(brick.x + brick.width // 2 - SHIELD_WIDTH // 2, brick.y, SHIELD_WIDTH, SHIELD_HEIGHT)
        elif random.random() < LASER_DROP_CHANCE:
            laser = pygame.Rect(brick.x + brick.width // 2 - SHIELD_WIDTH // 2, brick.y, SHIELD_WIDTH, SHIELD_HEIGHT)
    return shield, enlarge, laser

def update_powerups(shield, enlarge, laser, paddle, shield_active, enlarge_active, laser_active, shield_sound, enlarge_sound, laser_sound, countdown_start_time, SCREEN_HEIGHT):
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

    if laser:
        laser.y += 5
        if laser.colliderect(paddle):
            laser_active = True
            laser_sound.play()
            laser = None
        elif laser.y > SCREEN_HEIGHT:
            laser = None

    return shield, enlarge, laser, shield_active, enlarge_active, laser_active, countdown_start_time
