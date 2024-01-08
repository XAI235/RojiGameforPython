import os
import json
import pygame
from pygame.locals import *
from SystemMain.TitleScene import TitleScene
from SystemMain.GameScene import GameScene, CurrentGameScene

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
        
    def __del__(self):
        return 
    def initialize(self):
        with open('./Setting.json', encoding='utf-8') as jsonfile:
            self.game_config = json.load(jsonfile)
        with open('./File.json', encoding='utf-8') as jsonfile2:
            self.file_dir = json.load(jsonfile2)
        #with open('.\File.dat','r', encoding='utf-8') as f:
        #    line = f.readline()
        #    while line:
        #        words = line[:-1].split(',')
        #        self.MainPicture.setdefault(words[0], pygame.image.load(words[1]).convert_alpha())
        #        self.MP_rect.setdefault(words[0],self.MainPicture[words[0]].get_rect())
        #        line = f.readline()

        self.screen = pygame.display.set_mode((self.game_config["WindowWidth"],
                                               self.game_config["WindowHeight"]))  # 画面サイズ設定
        pygame.display.set_caption(self.game_config["TitleName"])                   # ウィンドウタイトル設定
        self.TS = TitleScene.TitleScene(self.game_config, self.file_dir)
        self.GS = GameScene.GameScene()
        return True

    def main_loop(self):
        self.TS.initialize()
        self.GS.initialize()
        self.running = True
        self.current_game_scene = CurrentGameScene.CurrentGameScene.TITLE_SCENE
        while(self.running):
            pygame.time.Clock().tick(30)
            self.TS.update(self.screen, self.current_game_scene)
            self.TS.draw()

            #self.GS.update()
            #self.GS.draw(self.screen)
            for event in pygame.event.get():
                if event.type == QUIT:                          # 終了ボタンを押した場合終了 セーブ警告とかなし
                    self.running = False

            pygame.display.update()                             # 画面更新 必ず必要
        
        pygame.quit()

    def finalize(self):
        return