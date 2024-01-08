import pygame
from pygame.locals import *

class MouseClass:
    def isMousePositionChecker(x1, y1, x2, y2):
        return (x1 <= pygame.mouse.get_pos()[0]
                and y1 <= pygame.mouse.get_pos()[1]
                and pygame.mouse.get_pos()[0] <= x2
                and pygame.mouse.get_pos()[1] <= y2)

    def isClickRightButton():
        isClick = pygame.mouse.get_pressed()
        return isClick[0]    # 右クリック

    def isClickLeftButton():
        isClick = pygame.mouse.get_pressed()
        return isClick[3]    # 左クリック