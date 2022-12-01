import pygame
import sys
from pygame.locals import *
from functions import *
import time
from functions import is_inside
from soundtest import *

class state:
    def __init__(self, screendim, startpos, background, mine):
        self.__screen = pygame.display.set_mode(screendim)
        self.__player = player(startpos[0], startpos[1])
        self.__keys = keyboard()
        self.__background = background
        self.__mines = []
        self.__bounds = self.__screen.get_rect().inflate(-250, -500).move(0, 220)
        self.__bottomScreen  = Rect(0, 0, 800, 220).move(0, 800)
        self.__topScreen = Rect(0, 0, 800, 220).move(0, -500)
        self.__pause = False
        self.__bullets = []
        self.__health = health()
        self.__guys = []
        self.__score = Score()
        self.bosses = []

    def render(self):
        if self.__pause == False:
            self.__background.render(self.__screen)
            for mine in self.__mines:
                mine.render(self.__screen)

            for bullet in self.__bullets:
                bullet.render(self.__screen)
            
            for guy in self.__guys:
                guy.render(self.__screen)
            
            for boss in self.bosses:
                boss.render(self.__screen)

            self.__player.render(self.__screen)
            self.__health.grey_render(self.__screen)
            self.__health.render(self.__screen)
            self.__score.render(self.__screen)
            pygame.draw.rect(self.__screen, (0, 255, 0), self.__bounds, 1) # border for debugging
            pygame.draw.rect(self.__screen, (0, 255, 255), self.__bottomScreen, 1) # border for debugging
            pygame.draw.rect(self.__screen, (255, 0, 255), self.__topScreen, 1) # border for debugging
            pygame.display.flip()

    def pause(self, lastP):
        if lastP > 10:
            self.__pause = not self.__pause
            return 0
        else:
            return lastP
    
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
    
    def change_player_health(self, x):
        self.__health.change_health(x)
    
    def get_health(self):
        return self.__health.get_health()

    def create_bullet(self, bullet):
        if self.__pause == False:
            self.__bullets.append(bullet)

            for check in self.__bullets:
                if not check == bullet:
                    if touches(bullet.get_rect().inflate(5,50), check.get_rect().inflate(0,50)):
                        del self.__bullets[len(self.__bullets)-1]
                
    
    def get_bullets(self):
        return self.__bullets
    
    def remove_bullet(self, bullet):
        self.__bullets.remove(bullet)
    
    def update_bullets(self, x, y):
        if self.__pause == False:
            for bullet in self.__bullets:
                bullet.change_pos(x, y)

    def get_topScreen(self):
        return self.__topScreen

    def create_guy(self, guy):
        if self.__pause == False:
            self.__guys.append(guy)

    def update_guys(self, x, y):
        if self.__pause == False:
            for guy in self.__guys:
                if guy.get_dead():
                    guy.change_pos(x, y)
                else:
                    guy.change_pos(x, y + 3 + y - 5)
    
    def get_guys(self):
        return self.__guys
    
    def remove_guy(self, guy):
        for check in self.__guys:
            if check == guy:
                self.__guys.remove(check)
    
    def change_guy_health(self, guy, x):
        guy.change_health(x)

    def kill_guy(self, guy):
        guy.die()

    def create_boss(self, boss):
        if self.__pause == False:
            self.bosses.append(boss)
    
    def update_bosses(self, x, y):
        if self.__pause == False:
            for boss in self.bosses:
                if boss.get_dead():
                    boss.change_pos(x, y*8)
                else:
                    boss.change_pos(x, y)
    
    def get_bosses(self):
        return self.bosses
    
    def remove_boss(self, boss):
        self.bosses.remove(boss)
    
    def change_boss_health(self, boss, x):
        boss.change_health(x)
    
    def kill_boss(self, boss):
        boss.die()
    




# ---------------------------------- #
# Object classes
# ---------------------------------- #






    def update_score(self, x):
        self.__score.update_score(x)

class player:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__image = pygame.image.load('./images/small-minigun-car.png')
        self.__rect = self.__image.get_rect(topleft=(self.__x, self.__y))
        self.__image = pygame.transform.scale(self.__image, (80, 160))
        

    def render(self, screen):
        screen.blit(self.__image, (self.__x, self.__y))
        pygame.draw.rect(screen, (255, 0, 0), self.__rect, 1) # for debugging, remove later
        self.__image = pygame.transform.scale(self.__image, (80, 160))
    
    
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
        expl1 = sound_library(r"./sounds")
        expl1.play_random_explosion()
        self.__image = pygame.image.load('./images/explosion.png')
        self.__image = pygame.transform.scale(self.__image, (50, 50))
        self.__exploded = True

    def reset_mine(self):
        self.__image = pygame.image.load('./images/mine.png')
        self.__image = pygame.transform.scale(self.__image, (50, 50))

class bullet:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__rect = pygame.Rect(self.__x, self.__y, 3, 10)

    def render(self, screen):
        self.__rect = pygame.Rect(self.__x, self.__y, 3, 10)
        pygame.draw.rect(screen, (255, 0, 0), self.__rect, 5)

    def change_pos(self, x, y):
        self.__x += x
        self.__y += y

    def get_rect(self):
        return self.__rect

class health:
    def __init__(self):
        self.__health = 200
        self.__rect = pygame.Rect(10, 10, self.__health, 25)
        self.__bar = pygame.Rect(10, 10, 200, 25)

    def render(self, screen):
        if self.__health > 100:
            pygame.draw.rect(screen, (0, 255, 0), self.__rect, 25)
        elif self.__health <= 100 and self.__health > 50:
            pygame.draw.rect(screen, (255, 255, 0), self.__rect, 25)
        elif self.__health <= 50:
            pygame.draw.rect(screen, (255, 0, 0), self.__rect, 25)
    def grey_render(self, screen):
        pygame.draw.rect(screen, (100, 100, 100), self.__bar, 25)

    def get_health(self):
        return self.__health
    
    def change_health(self, x):
        self.__health += x
        self.__rect = pygame.Rect(10, 10, self.__health, 25)

class guy:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__image = pygame.image.load('./images/zombie.png')
        self.__image = pygame.transform.scale(self.__image, (100, 100))
        #rotate image
        self.__image = pygame.transform.rotate(self.__image, 180)
        self.__rect = self.__image.get_rect(topleft=(self.__x, self.__y))
        self.__health = 100
        self.__healthRect = pygame.Rect(self.__x + 15, self.__y-10, self.__health/5, 5)
        self.__healthBar = pygame.Rect(self.__x + 15, self.__y-10, 20, 5)
        self.__dead = False

    def render(self, screen):
        self.__healthRect = pygame.Rect(self.__x + 15, self.__y-10, self.__health/5, 5)
        self.__healthBar = pygame.Rect(self.__x + 15, self.__y-10, 20, 5)

        self.__image = pygame.transform.scale(self.__image, (50, 50))
        screen.blit(self.__image, (self.__x, self.__y))
        pygame.draw.rect(screen, (255, 0, 0), self.__rect, 1) # for debugging, remove later
        
        if self.__health > 0:
            pygame.draw.rect(screen, (100, 100, 100), self.__healthBar, 25)
        
        if self.__health > 50:
            pygame.draw.rect(screen, (0, 255, 0), self.__healthRect, 25)
        elif self.__health <= 50 and self.__health > 25:
            pygame.draw.rect(screen, (255, 255, 0), self.__healthRect, 25)
        elif self.__health <= 25:
            pygame.draw.rect(screen, (255, 0, 0), self.__healthRect, 25)
        
        
    
    
    def change_pos(self, x, y):
        self.__x += x
        self.__y += y
        self.__rect = self.__image.get_rect(topleft=(self.__x, self.__y))

    def change_health(self, x):
        self.__health += x
    
    def get_health(self):
        return self.__health

    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y
    
    def get_rect(self):
        return self.__rect

    def die(self):
        self.__health = 0
        self.__dead = True
        self.__image = pygame.image.load('./images/bloodSplatter.png')
        self.__image = pygame.transform.scale(self.__image, (50, 50))

    def get_dead(self):
        return self.__dead
        
class Score:
    def __init__(self):
        self.__score = 0
        self.__rect = pygame.Rect(490, 10, 300, 50)

    def render(self, screen):
        font = pygame.font.SysFont('Arial', 30)
        text = font.render('Score: ' + str(round(self.__score)), True, (255, 255, 255))
        self.__rect = pygame.draw.rect(screen, (0, 0, 0), self.__rect, 25)
        screen.blit(text, (490, 10))
        pygame.draw.rect(screen, (255, 0, 0), self.__rect, 1)

    def get_score(self):
        return self.__score
    

    def update_score(self, x):
        self.__score += x

class boss:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__image = pygame.image.load('./images/boss.png')
        self.__image = pygame.transform.scale(self.__image, (300, 300))
        self.__rect = self.__image.get_rect(topleft=(self.__x, self.__y)).inflate(-80, -80)
        self.__health = 1000
        self.__healthRect = pygame.Rect(self.__x + 50, self.__y, self.__health/5, 5)
        self.__healthBar = pygame.Rect(self.__x + 50, self.__y, 200, 5)
        self.__dead = False

    def render(self, screen):
        self.__healthRect = pygame.Rect(self.__x + 50, self.__y, self.__health/5, 5)
        self.__healthBar = pygame.Rect(self.__x + 50, self.__y, 200, 5)

        self.__image = pygame.transform.scale(self.__image, (300, 300))
        screen.blit(self.__image, (self.__x, self.__y))
        pygame.draw.rect(screen, (255, 0, 0), self.__rect, 1) # for debugging, remove later
        
        if self.__health > 0:
            pygame.draw.rect(screen, (100, 100, 100), self.__healthBar, 25)
        
        if self.__health > 500:
            pygame.draw.rect(screen, (0, 255, 0), self.__healthRect, 25)
        elif self.__health <= 500 and self.__health > 250:
            pygame.draw.rect(screen, (255, 255, 0), self.__healthRect, 25)
        elif self.__health <= 250:
            pygame.draw.rect(screen, (255, 0, 0), self.__healthRect, 25)
         
    def change_pos(self, x, y):
        self.__x += x
        self.__y += y
        self.__rect = self.__image.get_rect(topleft=(self.__x, self.__y)).inflate(-80, -80)

    def change_health(self, x):
        self.__health += x
    
    def get_health(self):
        return self.__health

    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y
    
    def get_dead(self):
        return self.__dead

    def get_rect(self):
        return self.__rect
    
    def die(self):
        self.__health = 0
        self.__dead = True
        self.__image = pygame.image.load('./images/bloodSplatter.png')
        self.__image = pygame.transform.scale(self.__image, (300, 300))
        self.__rect = self.__image.get_rect(topleft=(self.__x, self.__y)).inflate(100, 100)
