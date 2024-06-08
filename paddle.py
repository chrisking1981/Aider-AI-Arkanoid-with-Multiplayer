import pygame

class Paddle:
     def __init__(self, screen_width, screen_height, paddle_width=100, paddle_height=20, speed=10):
         self.rect = pygame.Rect((screen_width // 2) - (paddle_width // 2), screen_height - 30, paddle_width, paddle_height)
         self.speed = speed
         self.height = paddle_height

         self.screen_width = screen_width

     def move(self, dx):
         self.rect.x += dx
         if self.rect.x < 0:
             self.rect.x = 0
         if self.rect.x > self.screen_width - self.rect.width:
             self.rect.x = self.screen_width - self.rect.width

     def draw(self, screen, color, scale_x, scale_y, game):
         scaled_paddle = pygame.Rect(self.rect.x * scale_x, self.rect.y * scale_y, self.rect.width * scale_x, self.rect.height * scale_y)
         if game.enlarge_active:
             pygame.draw.rect(screen, (0, 0, 255), scaled_paddle)  # Blue color when enlarged
         elif game.laser_active:
             pygame.draw.rect(screen, (255, 0, 0), scaled_paddle)  # Red color when laser is active
             pygame.draw.rect(screen, color, scaled_paddle)
