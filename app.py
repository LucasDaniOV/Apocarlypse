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


def create_main_surface(state, time):
    #create a new mine with a random x value and y value of 1 
    #has a 5% chance of spawning a mine

    if random.randint(1, 1000) <= 5:
        state.create_mine(Mine(random.randint(120, 580), -100))

    #create a new guy with a random x value and y value of 1
    #has a 20% chance of spawning a guy
    if random.randint(1, 1000) <= 20:
        state.create_guy(guy(random.randint(120, 580), -100))

    #create a new boss with a random x value and y value of 1
    #has a 1% chance of spawning a boss
    if time > 20 and random.randint(1, 500) <= 1 and state.get_bosses() == []:
        state.create_boss(boss(random.randint(150, 400), -100))
    
    render_frame(state)

def render_frame(state):
    state.render()

def process_input(state, step, lastP):
    
    # Pause and unpause when p is pressed
    if state.is_key_down(K_p):
       lastP = state.pause(lastP)
    
    # Move and shoot at the same time
    
    elif state.is_key_down(K_LEFT) and state.is_key_down(K_SPACE):
        state.change_player_pos(-step, 0)
        shoot(state)
    elif state.is_key_down(K_RIGHT) and state.is_key_down(K_SPACE):
        state.change_player_pos(step, 0)
        shoot(state)
    elif state.is_key_down(K_UP) and state.is_key_down(K_SPACE):
        state.change_player_pos(0, -step)
        shoot(state)
    elif state.is_key_down(K_DOWN) and state.is_key_down(K_SPACE):
        state.change_player_pos(0, step)
        shoot(state)
    
    elif state.is_key_down(K_SPACE):
        shoot(state)
    
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
        state.pause()
    
    elif state.is_key_down(K_ESCAPE):
        pygame.quit()
        sys.exit()

    if state.is_key_down(K_SPACE):
        minigun.playsound("sfx/bullet_sfx")
    
    return lastP

def shoot(state):
    bulletspread = [-20, 30]
    state.create_bullet(bullet(state.get_player().get_x() + 33, state.get_player().get_y() + random.randint(bulletspread[0], bulletspread[1])))
    state.create_bullet(bullet(state.get_player().get_x() + 40, state.get_player().get_y() + random.randint(bulletspread[0], bulletspread[1])))
    state.create_bullet(bullet(state.get_player().get_x() + 46, state.get_player().get_y() + random.randint(bulletspread[0], bulletspread[1])))
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
    speed = 5
    lastP = 700

    start_time = 0
    time_elapsed = 0

    pygame.key.set_repeat(round(speed) -2)

    while True:
        clock.tick(60)
        game.updateKeys()
        for event in pygame.event.get(): 
            lastP = process_input(game, 1, lastP)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if lastP < 11:
            lastP += 1
    
        if game.is_key_down(K_RETURN):
            if game.get_startbanner():
                game.update_startbanner(False)
                start_time = pygame.time.get_ticks()
                time_elapsed = 0
                
        
        
        if not game.get_startbanner():
            time_elapsed = (pygame.time.get_ticks() - start_time)
        
        time_elapsed_sec = time_elapsed / 1000
        speed = 5 + time_elapsed_sec / 10
        if speed > 15:
            speed = 15
        print(time_elapsed_sec)

        if not game.get_startbanner():
            game.update_background(speed)
            game.update_mine(0, speed)
            game.update_bullets(0, -50)
            game.update_guys(0, speed)
        game.update_bosses(0, speed/8)

        checkMines(game)
        checkBullets(game)
        checkGuys(game)
        checkBosses(game)

        game.update_score(time_elapsed / 30000)


        if game.get_health() <= 0:
            #stop time and display score
            selfdeath = sound_library(r"./sounds")
            selfdeath.playsound("sfx/death")
            pygame.mixer.music.stop()
            game.pause2(True)
            game.update_endbanner(True)
            game.render_endbanner()
            pygame.display.flip()

            if game.is_key_down(K_RETURN):
                start_time = pygame.time.get_ticks()
                time_elapsed = 0
                game.update_endbanner(False)
                game = state(screendim, startpos, Background("./images/highway.png", y), mine)


        if game.get_health() <= 0:
            #stop time and display score

            game.pause2(True)
            game.update_endbanner(True)
            game.render_endbanner()
            pygame.display.flip()

            if game.is_key_down(K_RETURN):
                start_time = pygame.time.get_ticks()
                time_elapsed = 0
                game.update_endbanner(False)
                game = state(screendim, startpos, Background("./images/highway.png", y), mine)
        create_main_surface(game, time_elapsed_sec)

if __name__ == '__main__':
    main()    