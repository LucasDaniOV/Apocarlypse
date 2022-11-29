import pygame
import sys
from pygame.locals import *

class state:
    def __init__(self, screendim, startpos, background):
        self.__screen = pygame.display.set_mode(screendim)
        self.__player = player(startpos[0], startpos[1])
        self.__keys = keyboard()
        self.__background = background

    def render(self):
        self.__background.render(self.__screen)
        self.__player.render(self.__screen)
        pygame.display.flip()
    
    def updateKeys(self):
        self.__keys.update()

    def is_key_down(self, key):
        return self.__keys.is_key_down(key)
    
    def change_player_pos(self, x, y):
        self.__player.change_pos(x, y)

    def update_background(self, a):
        self.__background.update(a) 

class player:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__image = pygame.image.load('./images/car.webp')
        # self.rect = self.image.get_rect() | This is for collision detection later on, will be used in the future

        self.__image = pygame.transform.scale(self.__image, (200, 300))

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

class Background:
    def __init__(self, image_file, y=0):
        self.__image = pygame.image.load(image_file)
        self.__image = pygame.transform.scale(self.__image, (800, 600))
        self.__y = y

    def render(self, screen):
        screen.blit(self.__image, (0, self.__y))
        screen.blit(self.__image, (0, self.__y - self.__image.get_height()))

    def update(self, a):
        self.__y += a
        if self.__y > self.__image.get_height():
            self.__y = 0