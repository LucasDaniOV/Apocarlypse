import pygame
import sys
from pygame.locals import *
from pygame.display import flip

pygame.init()
screen = pygame.display.set_mode((1024, 768))

class player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 50)

class keyboard:
    def __init__(self):
        self.keys = pygame.key.get_pressed()

    def is_pressed(self, key):
        return self.keys[key]

def create_main_surface():
    dot = player(100, 100)
    render_frame(dot)

def render_frame(player):
    player.draw()
    flip()


def main():
    while True:
        create_main_surface()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        


if __name__ == '__main__':
    main()


