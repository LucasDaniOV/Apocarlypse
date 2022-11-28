import pygame
import sys
from pygame.locals import *

class state:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.player = player(100, 100)
        self.keys = keyboard()

    def render(self):
        self.screen.fill((0, 0, 0))
        self.player.render(self.screen)
        pygame.display.flip()

class player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('./images/car.png')
        # self.rect = self.image.get_rect() | This is for collision detection later on, will be used in the future

    def render(self, screen):
        # pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 50)
        screen.blit(self.image, (self.x, self.y))


class keyboard:
    def __init__(self):
        self.keys = pygame.key.get_pressed()

    def is_key_down(self, key):
        if self.keys[key]:
            return True

