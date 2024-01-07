import os,sys, random
import pygame
from ..MouseClass import MouseClass

class GameScene:
    def __init__(self) :
        self.MainPicture = {}
        self.MP_rect = {}
        self.MainPictureBuffer = []
        self.MP_rectBuffer=[]
        self.MP_Coordinate = []
        self.td = []
        self.isMSWindow = False
        self.Now_read_line = []
        self.current_line = 0
        return
    
    def __del__(self):
        self.td.close()
        return 
    
    def initialize(self) :
        with open('./File.dat','r', encoding='utf-8') as f:
            line = f.readline()
            while line:
                words = line[:-1].split(',')
                self.MainPicture[words[0]] = pygame.image.load(words[1]).convert_alpha()
                self.MP_rect[words[0]] = self.MainPicture[words[0]].get_rect()
                line = f.readline()
        self.td = open('./Data/text/Scenario_data.txt', encoding='utf-8')
        
        # 初期化段階で シナリオ部分まで読み込ませる。
        self.Now_read_line = self.td.readline()
        self.Now_read_line = self.Now_read_line.lstrip()
        while self.Now_read_line not in '@@Message' :
            self.lexicalAnalysis(self.Now_read_line)
            self.Now_read_line = self.td.readline()
            self.Now_read_line = self.Now_read_line.lstrip()
        return 0
    
    def update(self) :
        if MouseClass.MouseClass.isClickRightButton() :
            self.lexicalAnalysis(self.Now_read_line)
            self.Now_read_line = self.td.readline()
            self.Now_read_line = self.Now_read_line.lstrip()
        return 0
    
    def draw(self, Screen) :
        # 描画順番
        # 背景 → キャラ → テキストウィンドウ → セリフ
        for i in range(len(self.MainPictureBuffer)) :
                Screen.blit(self.MainPictureBuffer[i], self.MP_Coordinate[i], area=self.MP_rectBuffer[i])
        return 0

    def lexicalAnalysis(self, line) :
        words = line[:-1].split(' ')
        if words[0] == '@@drawgraph' :
            self.MainPictureBuffer.append(self.MainPicture[words[-1]])
            self.MP_rectBuffer.append(self.MP_rect[words[-1]])
            self.MP_Coordinate.append((int(words[1]),int(words[2])))
        elif words[0] == '@@TextWindow' :
            if words[1] == '1' :
                self.MainPictureBuffer.append(self.MainPicture[words[-1]])
                self.MP_rectBuffer.append(self.MP_rect[words[-1]])
                self.MP_Coordinate.append((0,600))
                self.isMSWindow = True
            elif words[1] == '0' :
                self.MainPictureBuffer.remove(self.MainPicture[words[-1]])
                self.MP_rectBuffer.remove(self.MP_rect[words[-1]])
                self.MP_Coordinate.remove((0,300))
                self.isMSWindow = False