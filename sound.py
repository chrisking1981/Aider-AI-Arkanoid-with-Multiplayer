import pygame
import numpy as np

def generate_sound(frequency, duration, volume=0.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 32767 * volume * np.sin(2 * np.pi * frequency * t)
    sound_array = np.array(wave, dtype=np.int16)
    stereo_sound_array = np.zeros((sound_array.shape[0], 2), dtype=np.int16)
    stereo_sound_array[:, 0] = sound_array  # Left channel
    stereo_sound_array[:, 1] = sound_array  # Right channel
    return pygame.sndarray.make_sound(stereo_sound_array)

paddle_hit_sound = generate_sound(440, 0.1)
brick_hit_sound = generate_sound(880, 0.1)
game_over_sound = generate_sound(220, 0.5)
laser_sound = generate_sound(1000, 0.1)
shield_sound = generate_sound(660, 0.1)
enlarge_sound = generate_sound(550, 0.1)
sticky_sound = generate_sound(700, 0.1)
