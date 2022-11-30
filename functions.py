import pygame

import sys
from pygame.locals import *
from pygame.display import flip
from classes import *

# Contains helper functions

def is_inside(rect1, rect2):
    return rect1.contains(rect2)

def touches(rect1, rect2):
    return rect1.colliderect(rect2)

def checkMines(game):
        mines = game.get_mines()
        player = game.get_player()

        for mine in mines:
            if not mine.get_exploded():
                if touches(player.get_rect(), mine.get_rect()):
                    mine.explode()
                    game.change_health(-20)

                if touches(mine.get_rect(), game.get_bottomScreen()):
                    game.remove_mine(mine)  
                
            if mine.get_exploded():
                if touches(mine.get_rect(), game.get_bottomScreen()):
                    game.remove_mine(mine)

def checkBullets(state):
    bullets = state.get_bullets()
    for bullet in bullets:
        if touches(bullet.get_rect(), state.get_topScreen()):
            state.remove_bullet(bullet)
        # if touches(bullet.get_rect(), player.get_rect()):
        #     game.remove_bullet(bullet)
        #     game.change_health(-10)