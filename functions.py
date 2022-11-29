import pygame

import sys
from pygame.locals import *
from pygame.display import flip
from classes import *

def is_inside(rect1, rect2):
    return rect1.contains(rect2)