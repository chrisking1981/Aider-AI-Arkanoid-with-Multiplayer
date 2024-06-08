import pygame
import random

class Ball:
     def __init__(self, screen_width, screen_height, paddle, ball_size=10, ball_speed=3):
         self.rect = pygame.Rect(paddle.rect.x + paddle.rect.width // 2 - ball_size // 2, paddle.rect.y - ball_size, ball_size, ball_size)
         self.dx = ball_speed * random.choice((1, -1))
         self.dy = ball_speed * random.choice((1, -1))
         self.screen_width = screen_width
         self.screen_height = screen_height

     def move(self):
         self.rect.x += self.dx
         self.rect.y += self.dy

         if self.rect.left <= 0 or self.rect.right >= self.screen_width:
             self.dx = -self.dx
         if self.rect.top <= 0:
             self.dy = -self.dy

     def draw(self, screen, color, scale_x, scale_y):
         scaled_ball = pygame.Rect(self.rect.x * scale_x, self.rect.y * scale_y, self.rect.width * scale_x, self.rect.height * scale_y)
         pygame.draw.ellipse(screen, color, scaled_ball)

     def stick_to_paddle(self, paddle):
         self.rect.x = paddle.rect.x + paddle.rect.width // 2 - self.rect.width // 2
         self.rect.y = paddle.rect.y - self.rect.height

     def launch(self):
         self.dy = -abs(self.dy)

     def collides_with_paddle(self, paddle):
         return self.rect.colliderect(paddle.rect)

     def bounce_off_paddle(self, paddle):
         self.dy = -self.dy
         self.rect.y = paddle.rect.y - self.rect.height

     def collides_with_brick(self, brick):
         return self.rect.colliderect(brick.rect)

     def bounce_off_brick(self):
         self.dy = -self.dy

     def is_out_of_bounds(self, screen_height):
         return self.rect.top > screen_height

     def collides_with_shield(self, screen_height):
         return self.rect.bottom >= screen_height

     def bounce_off_shield(self, screen_height):
         self.dy = -self.dy
         self.rect.y = screen_height - self.rect.height - 1
