import pygame
import sys
from pygame.locals import *
from functions import *
class state:
    def __init__(self, screendim, startpos):
        self.__screen = pygame.display.set_mode(screendim)
        self.__player = player(startpos[0], startpos[1])
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
        # if  self.__screen.get_width() > self.__player.get_x() + x > 0:
        #     if self.__screen.get_height() > self.__player.get_y() + y > 0:
        if is_inside(self.__screen.get_rect(), self.__player.get_rect().move(x, y)):
            self.__player.change_pos(x, y) 
        else:
            self.__player.change_pos(0, 0)
             
        
    

class player:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__image = pygame.image.load('./images/car.png')
        self.__rect = self.__image.get_rect(topleft=(self.__x, self.__y)) #| This is for collision detection later on, will be used in the future

    def render(self, screen):
        screen.blit(self.__image, (self.__x, self.__y))
        pygame.draw.rect(screen, (255, 0, 0), self.__rect, 1)
    
    
    def change_pos(self, x, y):
        self.__x += x
        self.__y += y
        self.__rect = self.__image.get_rect(topleft=(self.__x, self.__y))
        
    
    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y
    
    def get_rect(self):
        return self.__rect



class keyboard:
    def __init__(self):
        self.__keys = pygame.key.get_pressed()

    def is_key_down(self, key):
        if self.__keys[key]:
            return True
        
    def update(self):
        self.__keys = pygame.key.get_pressed()
    
