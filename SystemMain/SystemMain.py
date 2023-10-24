import sys, random
import pygame
from pygame.locals import *
import tkinter

class SystemMain:

    frm = None
    def __init__(self):
        #self.frm = tkinter.Tk()
        pygame.init()
    def __del__(self):
        return 

    def initialize(self, width, height,screensize, titlename):
        self.screen = pygame.display.set_mode((width, height))  # 画面サイズ設定
        pygame.display.set_caption(titlename)                   # ウィンドウタイトル設定
        #self.frm.geometry(screensize)s
        #self.frm.title(titlename)
        return True

    def systemmain(self):
        while(True):
            self.screen.fill((0,0,0,))                          # 背景色(ここをうまくやればフェードイン、フェードアウト作れる?)
            pygame.display.update()                             # 画面更新 必ず必要
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
        #self.frm.mainloop()

    def finalize(self):
        sys.exit