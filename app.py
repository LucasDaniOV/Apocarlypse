import pygame


# Initialize Pygame
pygame.init()

# Tuple representing width and height in pixels
screen_size = (1024, 768)

def create_main_surface():
    pygame.display.set_mode(screen_size)

def main():
    while True:
        create_main_surface()
        
main()