import pygame

def maintain_aspect_ratio(event):
    global SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN, ASPECT_RATIO
    SCREEN_WIDTH = event.w
    SCREEN_HEIGHT = event.h
    if SCREEN_WIDTH / SCREEN_HEIGHT > ASPECT_RATIO:
        SCREEN_WIDTH = int(SCREEN_HEIGHT * ASPECT_RATIO)
    else:
        SCREEN_HEIGHT = int(SCREEN_WIDTH / ASPECT_RATIO)
    SCREEN = pygame.display.set_mode((event.w, event.h), pygame.FULLSCREEN)
