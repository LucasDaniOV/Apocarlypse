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