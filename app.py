import pygame

import sys
from pygame.locals import *
from pygame.display import flip
from classes import *
from functions import *

# Initialize Pygame
pygame.init()

def create_main_surface(state):
    render_frame(state)

def render_frame(state):
    state.render()

def process_input(state, step):
    # Functions weird, needs fixing
    # if state.is_key_down(K_LEFT) and state.is_key_down(K_DOWN):
    #     state.change_player_pos(-100, -100)
    # elif state.is_key_down(K_LEFT) and state.is_key_down(K_UP):
    #     state.change_player_pos(-100, 100)
    # elif state.is_key_down(K_RIGHT) and state.is_key_down(K_DOWN):
    #     state.change_player_pos(100, -100)
    # elif state.is_key_down(K_RIGHT) and state.is_key_down(K_UP):
    #     state.change_player_pos(100, 100)
    
    if state.is_key_down(K_RIGHT):
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
    screendim = (800, 600)
    # is array to easily grab the x and y values
    startpos = [400, 300]
    game = state(screendim, startpos)
    while True:
        game.updateKeys()
        create_main_surface(game)
        for event in pygame.event.get():
            process_input(game, 50)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        


if __name__ == '__main__':
    main()


