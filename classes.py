import pygame
import sys
from pygame.locals import *
class state:
    def __init__(self):
        self.__screen = pygame.display.set_mode((800, 600))
        self.__player = player(100, 100)
        self.__keys = keyboard()

    def render(self):
        self.__screen.fill((0, 0, 0))
        self.__player.render(self.__screen)
        pygame.display.flip()
    
    def updateKeys(self):
        self.__keys.update()

    def is_key_down(self, key):
        return self.__keys.is_key_down(key)
    
    def change_player_pos(self, x, y):
        self.__player.change_pos(x, y)

class player:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__image = pygame.image.load('./images/car.png')
        # self.rect = self.image.get_rect() | This is for collision detection later on, will be used in the future

    def render(self, screen):
        screen.blit(self.__image, (self.__x, self.__y))
    
    def change_pos(self, x, y):
        self.__x += x
        self.__y += y


class keyboard:
    def __init__(self):
        self.__keys = pygame.key.get_pressed()

    def is_key_down(self, key):
        if self.__keys[key]:
            return True
        
    def update(self):
        self.__keys = pygame.key.get_pressed()
    
