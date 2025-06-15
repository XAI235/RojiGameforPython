import pygame
from pygame.locals import *

class MouseClass:
    def isMousePositionChecker(pos, x1 : int, y1 : int, x2: int, y2 : int):
        return (x1 <= pos()[0]
                and y1 <= pos()[1]
                and pos()[0] <= x2
                and pos()[1] <= y2)