import os,sys, random
import pygame

class GameScene:
    def __init__(self) :
        self.MainPicture = []
        self.MainPictureBuffer = []
        self.MP_rect = []
        self.MP_rectBuffer=[]
        return
    
    def init(self) :
        with open('.\File.dat', encoding='utf-8' ) as f:
             line = f.readline()
             while line:
                  words = line[:-1].sprit(',')
                  self.MainPicture[words[0]].append(pygame.image.load(words[1]).convert_alpha())
                  self.MP_rect[words[0]].append(self.MainPicture[words[0]].get_rect())
                  line = f.readline()
        with open('.\Data\text\Scenario_data.txt', encoding='utf-8') as TextData:
            self.td = TextData
        return 0
    
    def update() :
        return 0
    
    def draw(self, Screen) :
        # 描画順番
        # 背景 → キャラ → テキストウィンドウ → セリフ

        for i in range(len(self.MainPictureBuffer)) :
                Screen.blit(self.MainPictureBuffer[i], (0, 0), area=self.MP_rect[i])

        return 0


