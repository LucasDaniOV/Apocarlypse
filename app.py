import pygame
import sys
from pygame.locals import *
from pygame.display import flip
from classes import *

pygame.init()
screen = pygame.display.set_mode((1024, 768))
dot = player(100, 100)
keys = keyboard()

def create_main_surface(player):
    render_frame(player)

def render_frame(player):
    player.draw(screen)
    flip()

def process_input(player):
    if keys.is_key_down(K_RIGHT):
        player.x += 100
    if keys.is_key_down(K_LEFT):
        player.x -= 100
    if keys.is_key_down(K_UP):
        player.y -= 100
    if keys.is_key_down(K_DOWN):
        player.y += 100
    
    if keys.is_key_down(K_ESCAPE):
        pygame.quit()
        sys.exit()
    
    
def main():
    while True:
        process_input(dot)
        create_main_surface(dot)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        


if __name__ == '__main__':
    main()


