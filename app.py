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

# Initialize Pygame
pygame.init()

minigun = sound_library(r"./sounds")


def create_main_surface(state):
    #create a new mine with a random x value and y value of 1 
    #has a 5% chance of spawning a mine

    if random.randint(1, 1000) <= 5:
        state.create_mine(Mine(random.randint(120, 580), -100))

    #create a new guy with a random x value and y value of 1
    #has a 5% chance of spawning a guy
    if random.randint(1, 100) <= 5:
        state.create_guy(guy(random.randint(120, 580), -100))
    
    render_frame(state)

def render_frame(state):
    state.render()

def process_input(state, step, lastP):
    bulletspread = [-20, 30]
    # Pause and unpause when p is pressed
    if state.is_key_down(K_p):
       lastP = state.pause(lastP)
    
    # Move and shoot at the same time
    
    elif state.is_key_down(K_LEFT) and state.is_key_down(K_SPACE):
        state.change_player_pos(-step, 0)
        state.create_bullet(bullet(state.get_player().get_x() + 33, state.get_player().get_y() + random.randint(bulletspread[0], bulletspread[1])))
        state.create_bullet(bullet(state.get_player().get_x() + 40, state.get_player().get_y() + random.randint(bulletspread[0], bulletspread[1])))
        state.create_bullet(bullet(state.get_player().get_x() + 46, state.get_player().get_y() + random.randint(bulletspread[0], bulletspread[1])))
    elif state.is_key_down(K_RIGHT) and state.is_key_down(K_SPACE):
        state.change_player_pos(step, 0)
        state.create_bullet(bullet(state.get_player().get_x() + 33, state.get_player().get_y() + random.randint(bulletspread[0], bulletspread[1])))
        state.create_bullet(bullet(state.get_player().get_x() + 40, state.get_player().get_y() + random.randint(bulletspread[0], bulletspread[1])))
        state.create_bullet(bullet(state.get_player().get_x() + 46, state.get_player().get_y() + random.randint(bulletspread[0], bulletspread[1])))
    elif state.is_key_down(K_SPACE):
        state.create_bullet(bullet(state.get_player().get_x() + 33, state.get_player().get_y() + random.randint(bulletspread[0], bulletspread[1])))
        state.create_bullet(bullet(state.get_player().get_x() + 40, state.get_player().get_y() + random.randint(bulletspread[0], bulletspread[1])))
        state.create_bullet(bullet(state.get_player().get_x() + 46, state.get_player().get_y() + random.randint(bulletspread[0], bulletspread[1])))
    
    # Don't move if opposite keys are pressed
    elif state.is_key_down(K_LEFT) and state.is_key_down(K_RIGHT):
        state.change_player_pos(0, 0)
    elif state.is_key_down(K_UP) and state.is_key_down(K_DOWN):
        state.change_player_pos(0, 0)

    # Diagonal
    elif state.is_key_down(K_LEFT) and state.is_key_down(K_DOWN):
        state.change_player_pos(-step, step)
    elif state.is_key_down(K_LEFT) and state.is_key_down(K_UP):
        state.change_player_pos(-step, -step)
    elif state.is_key_down(K_RIGHT) and state.is_key_down(K_DOWN):
        state.change_player_pos(step, step)
    elif state.is_key_down(K_RIGHT) and state.is_key_down(K_UP):
        state.change_player_pos(step, -step)
        
    # Axis
    elif state.is_key_down(K_RIGHT):
        state.change_player_pos(step, 0)
    elif state.is_key_down(K_LEFT):
        state.change_player_pos(-step, 0)  
    elif state.is_key_down(K_UP):
        state.change_player_pos(0, -step)
    elif state.is_key_down(K_DOWN):
        state.change_player_pos(0, step)
    
    # Pause and unpause when p is pressed
    elif state.is_key_down(K_p):
        pygame.time.wait(800)
        pygame.K_PAUSE()
    
    elif state.is_key_down(K_ESCAPE):
        pygame.quit()
        sys.exit()

    if state.is_key_down(K_SPACE):
        minigun.playsound("sfx/bullet_sfx")
    
    return lastP

def main():
    # infinite loop bgm
    pygame.mixer.music.play(loops=-1)
    #pygame.mixer.music.play(loops = -1)
    # Create the state
    screendim = (800, 800)
    # is array to easily grab the x and y values
    startpos = [360, 550]

    y = 0
    mine = Mine(300, 0)
    game = state(screendim, startpos, Background("./images/highway.png", y), mine)
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    speed = 5
    lastP = 700
    pygame.key.set_repeat(round(speed) -2)

    while True:
        clock.tick(60)
        game.updateKeys()
        create_main_surface(game)
        for event in pygame.event.get(): 
            lastP = process_input(game, 1, lastP)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        lastP += 1
        if game.get_health() <= 0:    
            selfdeath = sound_library(r"./sounds")
            selfdeath.playsound("sfx/death")
            pygame.mixer.music.stop()
            time.sleep(5)
            pygame.quit()
            sys.exit()
        time_elapsed = (pygame.time.get_ticks() - start_time)
        time_elapsed_sec = time_elapsed / 1000
        speed = 5 + time_elapsed_sec / 10
        if speed > 20:
            speed = 20
        print(time_elapsed_sec)
        game.update_background(speed)
        game.update_mine(0, speed)
        game.update_bullets(0, -50)
        game.update_guys(0, speed)

        checkMines(game)
        checkBullets(game)
        checkGuys(game)

        game.update_score(time_elapsed / 30000)

if __name__ == '__main__':
    main()