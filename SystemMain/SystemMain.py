import os,sys, random
import pygame
from pygame.locals import *

#os.path.abspath(__file__) : pythonファイルが存在する絶対パスを取得
#os.path.dirname(): 入力したパスの一つ上の階層のパスを取得

ROOTPATH = os.path.dirname(os.path.abspath(__file__))
CFGPATH = os.path.dirname(ROOTPATH)

#sys.path.append() ：入力したパスをpythonファイルの探索パスに追加する

#sys.path.append(CFGPATH)

class SystemMain:
    def __init__(self):
        pygame.init()
    def __del__(self):
        return 

    def initialize(self, width, height,screensize, titlename):
        self.screen = pygame.display.set_mode((width, height))  # 画面サイズ設定
        pygame.display.set_caption(titlename)                   # ウィンドウタイトル設定
        self.background = pygame.image.load(os.path.normpath(os.path.join(CFGPATH,'Data','image','menu.png'))) # とりあえずここ、画像クラスを作った方がよいのかもしれない?
        return True

    def systemmain(self):

        pygame.mixer.music.load(os.path.normpath(os.path.join(CFGPATH,'Data','sound','title.wav'))) # BGM読み込み
        pygame.mixer.music.set_volume(0.1)                  # 10%にとりあえず設定

        while(True):
            if(not pygame.mixer.music.get_busy()) :             #これでBGMがなっているかの判定
                pygame.mixer.music.play(-1)
            
            self.screen.fill((0,0,0,))                          # 背景色(ここをうまくやればフェードイン、フェードアウト作れる?)
            self.screen.blit(self.background,(0,0))
            
            for event in pygame.event.get():
                
                if event.type == QUIT:                          # 終了ボタンを押した場合終了 セーブ警告とかなし
                    pygame.quit()
            
            pygame.display.update()                             # 画面更新 必ず必要
                    
    def finalize(self):
        sys.exit