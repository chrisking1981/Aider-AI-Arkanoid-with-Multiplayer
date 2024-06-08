import pygame
 import numpy as np

 class SoundManager:
     def __init__(self):
         self.paddle_hit_sound = self.generate_sound(440, 0.1)
         self.brick_hit_sound = self.generate_sound(880, 0.1)
         self.game_over_sound = self.generate_sound(220, 0.5)
         self.laser_sound = self.generate_sound(1000, 0.1)
         self.shield_sound = self.generate_sound(660, 0.1)
         self.enlarge_sound = self.generate_sound(550, 0.1)
         self.sticky_sound = self.generate_sound(700, 0.1)

     @staticmethod
     def generate_sound(frequency, duration, volume=0.5, sample_rate=44100):
         t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
         wave = 32767 * volume * np.sin(2 * np.pi * frequency * t)
         sound_array = np.array(wave, dtype=np.int16)
         stereo_sound_array = np.zeros((sound_array.shape[0], 2), dtype=np.int16)
         stereo_sound_array[:, 0] = sound_array  # Left channel
         stereo_sound_array[:, 1] = sound_array  # Right channel
         return pygame.sndarray.make_sound(stereo_sound_array)