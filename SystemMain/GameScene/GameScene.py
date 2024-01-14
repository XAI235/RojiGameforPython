import os,sys, random
import pygame
from SystemMain.MouseClass import MouseClass

class GameScene:
    def __init__(self) :
        self.MainPicture :dict = {}  # メイン画像
        self.MP_rect :dict = {}      # メイン画像サイズ
        self.MainPictureBuffer :list = [] # メイン画像　バッファ
        self.MP_rectBuffer :list =[] # メイン画像のサイズ
        self.MP_Coordinate :list = [] # メイン画像の座標
        self.td : list = [] # テキストデータ群
        # 1ビット目 : メッセージウィンドウ
        # 2ビット目 : ネームプレートウィンドウ
        self.isMSWindow : int = 0b00
        self.Now_read_line : str = '' # 現在読み込んだテキストデータのラインデータ
        self.current_line : int = 0 # 読み込んだテキストデータの行数
        return
    
    def __del__(self):
        return 
    
    def initialize(self) :
        with open('./File.dat','r', encoding='utf-8') as f:
            line : str = f.readline()
            while line:
                words = line[:-1].split(',')
                self.MainPicture[words[0]] = pygame.image.load(words[1]).convert_alpha()
                self.MP_rect[words[0]] = self.MainPicture[words[0]].get_rect()
                line = f.readline()
        
        with open('./Data/text/Scenario_data.txt', encoding='utf-8') as f:
            line :str = f.readline()
            while line :
                self.td.append(line)
                line = f.readline()
        
        # 初期化段階で シナリオ部分まで読み込ませる。
        self.Now_read_line = self.td[self.current_line]
        self.Now_read_line = self.Now_read_line.lstrip()
        self.current_line += 1
        while self.Now_read_line not in '@@Message' :
            self.lexicalAnalysis(self.Now_read_line)
            self.Now_read_line = self.td[self.current_line]
            self.Now_read_line = self.Now_read_line.lstrip()
            self.current_line += 1
        return 0
    
    def update(self) :
        if MouseClass.MouseClass.isClickRightButton() :
            self.lexicalAnalysis(self.Now_read_line)
            self.Now_read_line = self.td.readline()
            self.Now_read_line = self.Now_read_line.lstrip()
        return 0
    
    def draw(self, Screen :pygame.surface.Surface) :
        # 描画順番
        # 背景 → キャラ → テキストウィンドウ → セリフ
        for i in range(len(self.MainPictureBuffer)) :
                Screen.blit(self.MainPictureBuffer[i], self.MP_Coordinate[i], area=self.MP_rectBuffer[i])
        return 0

    def lexicalAnalysis(self, line : str) :
        words = line[:-1].split(' ')
        if words[0] == '@@drawgraph' :
            self.MainPictureBuffer.append(self.MainPicture[words[-1]])
            self.MP_rectBuffer.append(self.MP_rect[words[-1]])
            self.MP_Coordinate.append((int(words[1]),int(words[2])))
        elif words[0] == '@@TextWindow' :
            if words[1] == '1' :
                if self.isMSWindow & 0b10 > 0 : # ネームプレートがあるときは格納位置はネームプレートの前
                    self.MainPictureBuffer.insert(-2, self.MainPicture[words[-1]])
                    self.MP_rectBuffer.insert(-2, self.MP_rect[words[-1]])
                    if words[-1] == 'LEFT' :
                        self.MP_Coordinate.append(-2,(0,600))
                    self.isMSWindow = self.isMSWindow | 0b01
                else : 
                    self.MainPictureBuffer.append(self.MainPicture[words[-1]])
                    self.MP_rectBuffer.append(self.MP_rect[words[-1]])
                    self.MP_Coordinate.append((0,600))
                    self.isMSWindow = self.isMSWindow | 0b10
            elif words[1] == '0' :
                self.MainPictureBuffer.remove(self.MainPicture[words[-1]])
                self.MP_rectBuffer.remove(self.MP_rect[words[-1]])
                self.MP_Coordinate.remove((0,300))
                self.isMSWindow = self.isMSWindow & 0b01
        #elif words[0] == '@@NamePlate' :
        #    if words[1] == 'namewindow_kanade' :
