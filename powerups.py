import pygame
import random

# Power-ups
SHIELD_WIDTH = 20
SHIELD_HEIGHT = 20
SHIELD_SIZE = 20
LASER_SIZE = 20
LASER_DROP_CHANCE = 0.1
STICKY_SIZE = 20
STICKY_DROP_CHANCE = 0.15

def handle_powerups(brick, paddle, shield, enlarge, laser, shield_active, enlarge_active, laser_active, shield_sound, enlarge_sound, laser_sound):
    if not (shield or enlarge or laser):
        powerups = ['shield', 'enlarge', 'laser', 'sticky']
        selected_powerup = random.choice(powerups)
        if selected_powerup == 'shield':
            shield = pygame.Rect(brick.x + brick.width // 2 - SHIELD_SIZE // 2, brick.y, SHIELD_SIZE, SHIELD_SIZE)
        elif selected_powerup == 'enlarge':
            enlarge = pygame.Rect(brick.x + brick.width // 2 - SHIELD_SIZE // 2, brick.y, SHIELD_SIZE, SHIELD_SIZE)
        elif selected_powerup == 'laser':
            laser = pygame.Rect(brick.x + brick.width // 2 - LASER_SIZE // 2, brick.y, LASER_SIZE, LASER_SIZE)
    return shield, enlarge, laser, sticky

def update_powerups(shield, enlarge, laser, sticky, paddle, shield_active, enlarge_active, laser_active, sticky_active, shield_sound, enlarge_sound, laser_sound, sticky_sound, countdown_start_time, SCREEN_HEIGHT):
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

    if sticky:
        sticky.y += 5
        if sticky.colliderect(paddle):
            sticky_active = True
            sticky_sound.play()
            sticky = None
        elif sticky.y > SCREEN_HEIGHT:
            sticky = None

    return shield, enlarge, laser, sticky, shield_active, enlarge_active, laser_active, sticky_active, countdown_start_time

def draw_powerups(screen, font, shield, enlarge, laser, sticky):
    if shield:
        pygame.draw.rect(screen, GREEN, shield)
        text = font.render("S", True, WHITE)
        screen.blit(text, (shield.x + 5, shield.y + 5))

    if enlarge:
        pygame.draw.rect(screen, BLUE, enlarge)
        text = font.render("E", True, WHITE)
        screen.blit(text, (enlarge.x + 5, enlarge.y + 5))

    if laser:
        pygame.draw.rect(screen, RED, laser)
        text = font.render("L", True, WHITE)
        screen.blit(text, (laser.x + 5, laser.y + 5))

# Shield constants
SHIELD_WIDTH = 20
SHIELD_HEIGHT = 20
SHIELD_SIZE = 20
SHIELD_DROP_CHANCE = 0.3

def handle_shield(brick, shield):
    if not shield:
        drop_chance = random.random()
        if drop_chance < SHIELD_DROP_CHANCE:
            shield = pygame.Rect(brick.x + brick.width // 2 - SHIELD_SIZE // 2, brick.y, SHIELD_SIZE, SHIELD_SIZE)
    return shield

def update_shield(shield, paddle, shield_active, shield_sound, countdown_start_time, SCREEN_HEIGHT):
    if shield:
        shield.y += 5
        if shield.colliderect(paddle):
            shield_active = True
            shield_sound.play()
            shield = None
            countdown_start_time = pygame.time.get_ticks()
        elif shield.y > SCREEN_HEIGHT:
            shield = None
    return shield, shield_active, countdown_start_time
# Laser constants
LASER_COOLDOWN = 125  # Cooldown period in milliseconds

def shoot_laser(paddle, lasers, last_shot_time, cooldown, laser_sound):
    current_time = pygame.time.get_ticks()
    if current_time - last_shot_time >= cooldown:
        laser = pygame.Rect(paddle.x + paddle.width // 2 - 2, paddle.y - 20, 4, 20)
        pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), laser)  # Draw the laser in red
        lasers.append(laser)
        laser_sound.play()
        return current_time
    return last_shot_time

def update_lasers(lasers, bricks, brick_hit_sound, paddle, shield, enlarge, laser, shield_active, enlarge_active, laser_active, shield_sound, enlarge_sound, laser_sound):
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
                    shield, enlarge, laser = handle_powerups(brick, paddle, shield, enlarge, laser, shield_active, enlarge_active, laser_active, shield_sound, enlarge_sound, laser_sound)
                    break
    return lasers, shield, enlarge, laser
    return lasers
# Enlarge constants
ENLARGE_DROP_CHANCE = 0.2

def handle_enlarge(brick, enlarge):
    if not enlarge:
        drop_chance = random.random()
        if drop_chance < ENLARGE_DROP_CHANCE:
            enlarge = pygame.Rect(brick.x + brick.width // 2 - SHIELD_SIZE // 2, brick.y, SHIELD_SIZE, SHIELD_SIZE)
    return enlarge

def update_enlarge(enlarge, paddle, enlarge_active, enlarge_sound, SCREEN_HEIGHT):
    if enlarge:
        enlarge.y += 5
        if enlarge.colliderect(paddle):
            enlarge_active = True
            enlarge_sound.play()
            enlarge = None
        elif enlarge.y > SCREEN_HEIGHT:
            enlarge = None
    return enlarge, enlarge_active
    if sticky:
        pygame.draw.rect(screen, YELLOW, sticky)
        text = font.render("T", True, WHITE)
        screen.blit(text, (sticky.x + 5, sticky.y + 5))
