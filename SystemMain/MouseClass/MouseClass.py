import os,sys, random
import pygame
from pygame.locals import *

class MouseClass:
    def isMousePositionChecker(x1, y1, x2, y2):
        if x1 <= pygame.mouse.get_pos()[0] and y1 <= pygame.mouse.get_pos()[1] and pygame.mouse.get_pos()[0] <= x2 and pygame.mouse.get_pos()[1] <= y2:
            return True
        return False

    def isClickRightButton():
        isClick = pygame.mouse.get_pressed()
        if isClick[0] :    # 右クリック
            return True
        return False
        
    def isClickLeftButton():
        isClick = pygame.mouse.get_pressed()
        if isClick[3] :    # 左クリック
            return True
        return False