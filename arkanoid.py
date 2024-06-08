import pygame
import sys
import random
import numpy as np

# Initialize Pygame
pygame.init()

from sound import SoundManager
from start_screen import show_start_screen
from colors import BLACK, WHITE, BLUE, RED, GREEN, YELLOW
from screen import maintain_aspect_ratio
from paddle import Paddle
from ball import Ball
from brick import Brick
from powerups import PowerUpManager
from laser import Laser

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ASPECT_RATIO = SCREEN_WIDTH / SCREEN_HEIGHT
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Arkanoid")
sound_manager = SoundManager()

paddle_hit_sound = sound_manager.paddle_hit_sound
brick_hit_sound = sound_manager.brick_hit_sound
game_over_sound = sound_manager.game_over_sound
laser_sound = sound_manager.laser_sound
shield_sound = sound_manager.shield_sound
enlarge_sound = sound_manager.enlarge_sound
sticky_sound = sound_manager.sticky_sound

class Game:
     def __init__(self):
         self.screen = SCREEN
         self.screen_width = SCREEN_WIDTH
         self.screen_height = SCREEN_HEIGHT
         self.clock = pygame.time.Clock()
         self.font = pygame.font.Font(None, 24)
         self.paddle = Paddle(SCREEN_WIDTH, SCREEN_HEIGHT)
         self.ball = Ball(SCREEN_WIDTH, SCREEN_HEIGHT, self.paddle)
         self.bricks = Brick.create_bricks()
         self.powerup_manager = PowerUpManager()
         self.ball_stuck = True
         self.lasers = []
         self.paddle.rect.width = 100  # Reset paddle width to default
         self.paddle_hit_sound = paddle_hit_sound
         self.brick_hit_sound = brick_hit_sound
         self.game_over_sound = game_over_sound
         self.laser_sound = laser_sound
         self.shield_sound = shield_sound
         self.enlarge_sound = enlarge_sound
         self.sticky_sound = sticky_sound
         self.countdown_start_time = 0
         self.shield_active = False
         self.enlarge_active = False
         self.laser_active = False
         self.sticky_active = False
         self.last_shot_time = 0

     def reset(self):
         self.paddle = Paddle(SCREEN_WIDTH, SCREEN_HEIGHT)
         self.ball = Ball(SCREEN_WIDTH, SCREEN_HEIGHT, self.paddle)
         self.bricks = Brick.create_bricks()
         self.ball_stuck = True
         self.shield_active = False
         self.enlarge_active = False
         self.laser_active = False
         self.sticky_active = False
         self.last_shot_time = 0

     def handle_events(self):
         for event in pygame.event.get():
             if event.type == pygame.VIDEORESIZE:
                 maintain_aspect_ratio(event)
             if event.type == pygame.QUIT:
                 pygame.quit()
                 sys.exit()

     def update(self):
         keys = pygame.key.get_pressed()
         if keys[pygame.K_LEFT]:
             self.paddle.move(-self.paddle.speed)
         if keys[pygame.K_RIGHT]:
             self.paddle.move(self.paddle.speed)
         if keys[pygame.K_SPACE] and self.laser_active:
             self.shoot_laser()
             self.ball.stick_to_paddle(self.paddle)
             if keys[pygame.K_f]:
                 self.ball.launch()
                 self.ball_stuck = False
         else:
             self.ball.move()

         if self.ball.collides_with_paddle(self.paddle):
             self.ball.bounce_off_paddle(self.paddle)
             paddle_hit_sound.play()
         elif self.shield_active and self.ball.collides_with_shield(SCREEN_HEIGHT):
             self.ball.bounce_off_shield(SCREEN_HEIGHT)
             paddle_hit_sound.play()

         for brick in self.bricks[:]:
             if self.ball.collides_with_brick(brick):
                 self.ball.bounce_off_brick()
                 self.bricks.remove(brick)
                 brick_hit_sound.play()
                 self.powerup_manager.handle_powerups(brick, self.paddle, self)
                 break

         if self.ball.is_out_of_bounds(SCREEN_HEIGHT):
             game_over_sound.play()
             pygame.time.wait(2000)
             show_start_screen(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
             self.reset()

         self.powerup_manager.update(self.paddle, self)
         self.update_lasers()

     def draw(self):
         self.screen.fill(BLACK)
         self.paddle.draw(self.screen, WHITE, 1, 1, self)
         self.ball.draw(self.screen, WHITE, 1, 1)
         for brick in self.bricks:
             Brick.draw(self.screen, brick, BLUE, 1, 1)
         self.powerup_manager.draw(self.screen, self.font)
         self.draw_lasers()
         self.draw_shield()
         self.draw_timer()
         pygame.display.flip()

     def draw_shield(self):
         if self.shield_active:
             pygame.draw.rect(self.screen, GREEN, (0, SCREEN_HEIGHT - self.paddle.height, SCREEN_WIDTH, self.paddle.height))

     def draw_timer(self):
         remaining_time = self.get_remaining_time()
         timer_text = f"Shield: {remaining_time // 60000:02}:{(remaining_time % 60000) // 1000:02}" if self.shield_active else "Shield: 00:00"
         text = self.font.render(timer_text, True, WHITE)
         self.screen.blit(text, (10, 10))

     def get_remaining_time(self):
         elapsed_time = pygame.time.get_ticks() - self.countdown_start_time
         return max(0, 30000 - elapsed_time)

     def shoot_laser(self):
         if pygame.time.get_ticks() - self.last_shot_time > 500:  # 500 ms delay between shots
             laser = Laser(self.paddle.rect.centerx, self.paddle.rect.top)
             self.lasers.append(laser)
             self.last_shot_time = pygame.time.get_ticks()

     def update_lasers(self):
         for laser in self.lasers[:]:
             laser.move()
             if laser.rect.bottom < 0:
                 self.lasers.remove(laser)
             else:
                 for brick in self.bricks[:]:
                     if laser.rect.colliderect(brick.rect):
                         self.bricks.remove(brick)
                         self.lasers.remove(laser)
                         self.brick_hit_sound.play()
                         break

     def draw_lasers(self):
         for laser in self.lasers:
             laser.draw(self.screen)
     def run(self):
         show_start_screen(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
         while True:
             self.handle_events()
             self.update()
             self.draw()
             self.clock.tick(60)
         while True:
             self.handle_events()
             self.update()
             self.draw()
             self.clock.tick(60)

if __name__ == "__main__":
     game = Game()
     game.run()
