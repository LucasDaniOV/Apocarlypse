import pygame
import random
import sys
from pygame.locals import *
from pygame.display import flip
from classes import *
from functions import *
import random

# Initialize Pygame
pygame.init()

def create_main_surface(state):
    #create a new mine with a random x value and y value of 1 
    #has a 5% chance of spawning a mine

    if random.randint(1, 500) <= 2:
        state.create_mine(Mine(random.randint(120, 580), -100))
    
    render_frame(state)

def render_frame(state):
    state.render()

def process_input(state, step):

    # Pause and unpause when p is pressed
    if state.is_key_down(K_p):
        state.pause()
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
    
    
    elif state.is_key_down(K_ESCAPE):
        pygame.quit()
        sys.exit()


def main():
    # Create the state
    screendim = (800, 800)
    # is array to easily grab the x and y values
    startpos = [360, 600]

    y = 0
    mine = Mine(300, 0)
    game = state(screendim, startpos, Background("./images/highway.png", y), mine)
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    speed = 5
    pygame.key.set_repeat(3)

    while True:
        clock.tick(60)
        game.updateKeys()
        create_main_surface(game)
        for event in pygame.event.get():
            process_input(game, 1)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if game.get_health() <= 0:    
            time.sleep(5)
            pygame.quit()
            sys.exit()

        time_elapsed = pygame.time.get_ticks() - start_time
        game.update_background(speed)
        game.update_mine(0, speed)


        mines = game.get_mines()
        player = game.get_player()

        for mine in mines:
            if not mine.get_exploded():
                if touches(player.get_rect(), mine.get_rect()):
                    mine.explode()
                    game.change_health(-20)

                if touches (mine.get_rect(), game.get_bottomScreen()):
                    game.remove_mine(mine)  
                
            if mine.get_exploded():
                if touches (mine.get_rect(), game.get_bottomScreen()):
                    game.remove_mine(mine)

if __name__ == '__main__':
    main()
