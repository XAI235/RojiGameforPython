import os,sys, random
import pygame
from pygame.locals import *

class MouseClass:
    def isMousePositionChecker(x1, y1, x2, y2):
        if (x1, y1) <= pygame.mouse.get_pos() and pygame.mouse.get_pos() <= (x2,y2):
            print('OK')
            return True
        
        print('NG')
        return False
