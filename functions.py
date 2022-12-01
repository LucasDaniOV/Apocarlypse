import pygame
import random
import sys
from pygame.locals import *
from pygame.display import flip
from classes import * 
from functions import *
import random
from audio import *
import time
from app import *

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
                    game.change_player_health(-20)

                if touches(mine.get_rect(), game.get_bottomScreen()):
                    game.remove_mine(mine)  
                
            if mine.get_exploded():
                if touches(mine.get_rect(), game.get_bottomScreen()):
                    game.remove_mine(mine)

def checkGuys(game):
    guys = game.get_guys()
    player = game.get_player()
    bullets = game.get_bullets()
    for guy in guys:
        for bullet in bullets:
            if touches(bullet.get_rect(), guy.get_rect()):
                if guy.get_health() > 0:
                    game.change_guy_health(guy, -10)
                    game.remove_bullet(bullet)
        if touches(player.get_rect(), guy.get_rect()) and not guy.get_dead():
            if guy.get_health() > 0:
                game.kill_guy(guy)
                game.change_player_health(-10)

        if guy.get_health() <= 0 and not guy.get_dead():
            game.kill_guy(guy)
                
        
        if touches(guy.get_rect(), game.get_bottomScreen()):
            game.remove_guy(guy)
        

def checkBullets(state):
    bullets = state.get_bullets()
    for bullet in bullets:
        if touches(bullet.get_rect(), state.get_topScreen()):
            state.remove_bullet(bullet)


def checkBosses(game):
    bosses = game.get_bosses()
    player = game.get_player()
    bullets = game.get_bullets()
    for boss in bosses:
        for bullet in bullets:
            if touches(bullet.get_rect(), boss.get_rect()):
                if boss.get_health() > 0:
                    game.change_boss_health(boss, -10)
                    game.remove_bullet(bullet)
        if touches(player.get_rect(), boss.get_rect()) and not boss.get_dead():
            if boss.get_health() > 0:
                game.kill_boss(boss)
                game.change_player_health(-100)

        if boss.get_health() <= 0 and not boss.get_dead():
            game.kill_boss(boss)
                
        
        if touches(boss.get_rect(), game.get_bottomScreen().move(0, 300)):
            game.remove_boss(boss)


