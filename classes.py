import pygame
import sys
from pygame.locals import *
<<<<<<< HEAD

=======
from functions import *
>>>>>>> c3ce5383a61f0f358d68dbb83d7b048446ebfc67
class state:
    def __init__(self, screendim, startpos, background):
        self.__screen = pygame.display.set_mode(screendim)
        self.__player = player(startpos[0], startpos[1])
        self.__keys = keyboard()
        self.__background = background

    def render(self):
        self.__background.render(self.__screen)
        self.__player.render(self.__screen)
        pygame.draw.rect(self.__screen, (0, 255, 0), self.__screen.get_rect(), 1) # border for debugging
        pygame.display.flip()
    
    def updateKeys(self):
        self.__keys.update()

    def is_key_down(self, key):
        return self.__keys.is_key_down(key)
    
    def change_player_pos(self, x, y):
        if is_inside(self.__screen.get_rect(), self.__player.get_rect().move(x, y)):
            self.__player.change_pos(x, y) 
        else:
            match (x, y):
                case (x, 0):
                    while(is_inside(self.__screen.get_rect(), self.__player.get_rect().move(x/abs(x), 0))): 
                        self.__player.change_pos(x/abs(x), 0)
                case (0, y):
                    while(is_inside(self.__screen.get_rect(), self.__player.get_rect().move(0, y/abs(y)))):
                        self.__player.change_pos(0, y/abs(y))
                case (x, y):
                    while(is_inside(self.__screen.get_rect(), self.__player.get_rect().move(x/abs(x), y/abs(y)))):
                        self.__player.change_pos(x/abs(x), y/abs(y))
                
                
             
        
    

    def update_background(self, a):
        self.__background.update(a) 

class player:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__image = pygame.image.load('./images/car.png')
        self.__rect = self.__image.get_rect(topleft=(self.__x, self.__y))

        self.__image = pygame.transform.scale(self.__image, (200, 300))

    def render(self, screen):
        screen.blit(self.__image, (self.__x, self.__y))
        pygame.draw.rect(screen, (255, 0, 0), self.__rect, 1) # for debugging, remove later
    
    
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