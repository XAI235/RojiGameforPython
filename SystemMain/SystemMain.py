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
        background = pygame.image.load('.\Data\image\menu.png') # とりあえずここ、画像クラスを作った方がよいのかもしれない?
        pygame.mixer.music.load('.\Data\sound\\title.wav') # BGM読み込み
        pygame.mixer.music.set_volume(0.1)                  # 10%にとりあえず設定

        while(True):
            if(not pygame.mixer.music.get_busy()) :
                pygame.mixer.music.play(-1)
            self.screen.fill((0,0,0,))                          # 背景色(ここをうまくやればフェードイン、フェードアウト作れる?)
            self.screen.blit(background,(0,0))
            pygame.display.update()                             # 画面更新 必ず必要
            for event in pygame.event.get():
                if event.type == QUIT:                          # 終了ボタンを押した場合終了 セーブ警告とかなし
                    pygame.mixer.music.fadeout(2)
                    pygame.quit()
        #self.frm.mainloop()

    def finalize(self):
        sys.exit