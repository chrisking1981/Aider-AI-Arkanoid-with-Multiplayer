import pygame
import random

class PowerUpManager:
     SHIELD_WIDTH = 20
     SHIELD_HEIGHT = 20
     SHIELD_SIZE = 20
     LASER_SIZE = 20
     LASER_DROP_CHANCE = 0.1
     STICKY_SIZE = 20
     STICKY_DROP_CHANCE = 0.15

     def __init__(self):
         self.shield = None
         self.enlarge = None
         self.laser = None
         self.sticky = None

     def handle_powerups(self, brick, paddle, game):
         if not (self.shield or self.enlarge or self.laser or self.sticky):
             powerups = ['shield', 'enlarge', 'laser', 'sticky']
             selected_powerup = random.choice(powerups)
             if selected_powerup == 'shield':
                 self.shield = pygame.Rect(brick.rect.x + brick.rect.width // 2 - self.SHIELD_SIZE // 2, brick.rect.y, self.SHIELD_SIZE, self.SHIELD_SIZE)
             elif selected_powerup == 'enlarge':
                 self.enlarge = pygame.Rect(brick.rect.x + brick.rect.width // 2 - self.SHIELD_SIZE // 2, brick.rect.y, self.SHIELD_SIZE, self.SHIELD_SIZE)
             elif selected_powerup == 'laser':
                 self.laser = pygame.Rect(brick.rect.x + brick.rect.width // 2 - self.LASER_SIZE // 2, brick.rect.y, self.LASER_SIZE, self.LASER_SIZE)
         return self.shield, self.enlarge, self.laser, self.sticky

     def update(self, paddle, game):
         self.update_shield(paddle, game)
         self.update_enlarge(paddle, game)
         self.update_laser(paddle, game)
         self.update_sticky(paddle, game)

     def update_shield(self, paddle, game):
         if self.shield:
             self.shield.y += 5
             if self.shield.colliderect(paddle.rect):
                 game.shield_active = True
                 game.shield_sound.play()
                 self.shield = None
                 game.countdown_start_time = pygame.time.get_ticks()
             elif self.shield.y > game.screen_height:
                 self.shield = None

     def update_enlarge(self, paddle, game):
         if self.enlarge:
             self.enlarge.y += 5
             if self.enlarge.colliderect(paddle.rect):
                 if not game.enlarge_active:
                     game.enlarge_active = True
                     game.enlarge_sound.play()
                     paddle.rect.width *= 1.5  # Increase paddle width by 50%
                 self.enlarge = None
             elif self.enlarge.y > game.screen_height:
                 self.enlarge = None

     def update_laser(self, paddle, game):
         if self.laser:
             self.laser.y += 5
             if self.laser.colliderect(paddle.rect):
                 if not game.laser_active:
                     game.laser_active = True
                     game.laser_sound.play()
                 self.laser = None
             elif self.laser.y > game.screen_height:
                 self.laser = None

     def update_sticky(self, paddle, game):
         if self.sticky:
             self.sticky.y += 5
             if self.sticky.colliderect(paddle.rect):
                 game.sticky_active = True
                 game.sticky_sound.play()
                 self.sticky = None
             elif self.sticky.y > game.screen_height:
                 self.sticky = None

     def draw(self, screen, font):
         if self.shield:
             pygame.draw.rect(screen, (0, 255, 0), self.shield)
             text = font.render("S", True, (255, 255, 255))
             screen.blit(text, (self.shield.x + 5, self.shield.y + 5))

         if self.enlarge:
             pygame.draw.rect(screen, (0, 0, 255), self.enlarge)
             text = font.render("E", True, (255, 255, 255))
             screen.blit(text, (self.enlarge.x + 5, self.enlarge.y + 5))

         if self.laser:
             pygame.draw.rect(screen, (255, 0, 0), self.laser)
             text = font.render("L", True, (255, 255, 255))
             screen.blit(text, (self.laser.x + 5, self.laser.y + 5))

         if self.sticky:
             pygame.draw.rect(screen, (255, 255, 0), self.sticky)
             text = font.render("T", True, (255, 255, 255))
             screen.blit(text, (self.sticky.x + 5, self.sticky.y + 5))
class Laser:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 20)
        self.speed = 10

    def move(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
class Laser:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 20)
        self.speed = 10

    def move(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
class Laser:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 20)
        self.speed = 10

    def move(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
class Laser:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 20)
        self.speed = 10

    def move(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
