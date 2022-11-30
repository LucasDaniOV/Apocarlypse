import pygame
import sys
from pygame.locals import *
from functions import *
import time

class state:
    def __init__(self, screendim, startpos, background, mine):
        self.__screen = pygame.display.set_mode(screendim)
        self.__player = player(startpos[0], startpos[1])
        self.__keys = keyboard()
        self.__background = background
        self.__mines = []
        self.__bounds = self.__screen.get_rect().inflate(-250, -500).move(0, 220)
        self.__bottomScreen  = self.__screen.get_rect().inflate(0, -799).move(0, 390)
        self.__pause = False

    def render(self):
        if self.__pause == False:
            self.__background.render(self.__screen)
            for mine in self.__mines:
                mine.render(self.__screen)
            self.__player.render(self.__screen)
            pygame.draw.rect(self.__screen, (0, 255, 0), self.__bounds, 1) # border for debugging
            pygame.draw.rect(self.__screen, (0, 255, 255), self.__bottomScreen, 1) # border for debugging
            pygame.display.flip()

    def pause(self):
        self.__pause = not self.__pause
    
    def get_pause(self):
        return self.__pause
    
    def updateKeys(self):
        self.__keys.update()

    def is_key_down(self, key):
        return self.__keys.is_key_down(key)
    
    def change_player_pos(self, x, y):
        if self.__pause == False:
            if is_inside(self.__bounds, self.__player.get_rect().move(x, y)):
                self.__player.change_pos(x, y) 
            else:
                match (x, y):
                    case (x, 0):
                        while(is_inside(self.__bounds, self.__player.get_rect().move(x/abs(x), 0))): 
                            self.__player.change_pos(x/abs(x), 0)
                    case (0, y):
                        while(is_inside(self.__bounds, self.__player.get_rect().move(0, y/abs(y)))):
                            self.__player.change_pos(0, y/abs(y))
                    case (x, y):
                        while(is_inside(self.__bounds, self.__player.get_rect().move(x/abs(x), y/abs(y)))):
                            self.__player.change_pos(x/abs(x), y/abs(y))
    def update_background(self, a):
        if self.__pause == False:
            self.__background.update(a) 
    
    def create_mine(self, mine):
        if self.__pause == False:
            self.__mines.append(mine)

    def get_mines_len(self):
        return len(self.__mines)

    def get_mines(self):
        return self.__mines

    def get_bottomScreen(self):
        return self.__bottomScreen

    def get_player(self):
        return self.__player

    def update_mine(self, x, y):
        if self.__pause == False:
            for mine in self.__mines:
                mine.change_pos(x, y)
        
    def remove_mine(self, mine):
        self.__mines.remove(mine)
    
    def explode_mine(self, mine):
        mine.explode()

class player:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__image = pygame.image.load('./images/small-minigun-car.png')
        self.__rect = self.__image.get_rect(topleft=(self.__x, self.__y))

        #self.__image = pygame.transform.scale(self.__image, (200, 300))

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
        self.__image = pygame.transform.scale(self.__image, (800, 800))
        self.__y = y

    def render(self, screen):
        screen.blit(self.__image, (0, self.__y))
        screen.blit(self.__image, (0, self.__y - self.__image.get_height()))

    def update(self, a):
        self.__y += a
        if self.__y > self.__image.get_height():
            self.__y = 0

class Mine:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__image = pygame.image.load('./images/mine.png')
        self.__image = pygame.transform.scale(self.__image, (100, 100))
        self.__rect = self.__image.get_rect(topleft=(self.__x, self.__y))
        self.__exploded = False

    def render(self, screen):
        screen.blit(self.__image, (self.__x, self.__y))
        self.__image = pygame.transform.scale(self.__image, (50, 50))
        pygame.draw.rect(screen, (255, 0, 0), self.__rect, 1) # for debugging, remove later

    def get_rect(self):
        return self.__rect

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_exploded(self):
        return self.__exploded

    def change_pos(self, x, y):
        if self.__y > 800:
            self.__y = -100

        self.__x += x
        self.__y += y
        self.__rect = self.__image.get_rect(topleft=(self.__x, self.__y))

    def explode(self):
        self.__image = pygame.image.load('./images/explosion.png')
        self.__image = pygame.transform.scale(self.__image, (50, 50))
        self.__exploded = True

    def reset_mine(self):
        self.__image = pygame.image.load('./images/mine.png')
        self.__image = pygame.transform.scale(self.__image, (50, 50))