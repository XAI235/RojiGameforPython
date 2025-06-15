
import pygame
from abc import abstractmethod, ABC

# 抽象クラス
class basescene(ABC) : 
        @abstractmethod
        def __init__(self):
             pass
        
        def update(self):
            pass

        def draw(self) : 
            pass

        def mouse_event(self):
            pass
        
        def Changer_Scene(self):
            pass