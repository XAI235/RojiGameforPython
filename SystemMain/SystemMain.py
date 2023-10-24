import sys, random
import pygame
import tkinter

class SystemMain:

    frm = None
    def __init__(self):
        self.pygame.init()
    def __del__(self):
        return 

    def initialize(self, screensize,titlename):
        self.frm.geometry(screensize)
        self.frm.title(titlename)
        return True

    def systemmain(self):
        self.frm.mainloop()
        return

    def finalize(self):
        print(3+1)