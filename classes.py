import pygame
import sys
from pygame.locals import *


class player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 50)
        
class keyboard:
    def __init__(self):
        self.keys = pygame.key.get_pressed()

    def is_key_down(self, key):
        if self.keys[key]:
            return True

