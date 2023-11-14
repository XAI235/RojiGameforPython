import os,sys, random
import json
import pygame
from pygame.locals import *
from .MouseClass import MouseClass
import cv2

#os.path.abspath(__file__) : pythonファイルが存在する絶対パスを取得
#os.path.dirname(): 入力したパスの一つ上の階層のパスを取得

ROOTPATH = os.path.dirname(os.path.abspath(__file__))
CFGPATH = os.path.dirname(ROOTPATH)

# タイトル画面とかゲーム画面、コンフィグ画面に移行する際は、状態遷移で行った方がいいのかな?
# OP(ロゴ表示) -> タイトル画面 --->初めから
#                             |->ロード画面
#                             |->設定画面
#                             |->終了

class SystemMain:
    def __init__(self):
        pygame.init()
        with open(os.path.normpath(os.path.join(CFGPATH,'Setting.json')), encoding='utf-8') as jsonfile:
            self.json_data = json.load(jsonfile)
    def __del__(self):
        return 
    def initialize(self, width, height, titlename):
        self.screen = pygame.display.set_mode((self.json_data["windowWidth"], self.json_data["WindowHight"]))  # 画面サイズ設定
        pygame.display.set_caption(self.json_data["TitleName"])                   # ウィンドウタイトル設定
        return True
    def systemmain(self):
        self.background = pygame.image.load(os.path.normpath(os.path.join(CFGPATH,'Data','image','menu.png'))) # とりあえずここ、画像クラスを作った方がよいのかもしれない?
        self.running = True
        while(self.running):
            MouseClass.MouseClass.isMousePositionChecker(640,360,800,800)
            for event in pygame.event.get():
                if event.type == QUIT:                          # 終了ボタンを押した場合終了 セーブ警告とかなし
                    self.running = False
            pygame.display.update()                             # 画面更新 必ず必要
        
        pygame.quit()
                    
    def finalize(self):
        sys.exit