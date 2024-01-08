import os
import math
import pygame
from pygame.locals import *
from SystemMain.MouseClass import MouseClass

ROOTPATH = os.path.dirname(os.path.abspath(__file__))
FFGPATH = os.path.dirname(ROOTPATH)
CFGPATH = os.path.dirname(os.path.dirname(ROOTPATH))

class TitleScene :
    def __init__(self, game_config : dict , file_dir : dict):
         self.game_config : dict = game_config
         self.file_dir : dict = file_dir

    def initialize(self):
        self.time :list = []
        self.Button_Data : list = []
        self.rects_Button : list = []
        self.BackGround :pygame.surface.Surface = pygame.image.load(self.file_dir["Title"]).convert_alpha() # TitelScene専用の画像配列
        self.Button_Data.append(pygame.image.load(self.file_dir["Start"]).convert_alpha()) # TitelScene専用の画像配列
        self.Button_Data.append(pygame.image.load(self.file_dir["load"]).convert_alpha()) # TitelScene専用の画像配列
        self.Button_Data.append(pygame.image.load(self.file_dir["config"]).convert_alpha()) # TitelScene専用の画像配列
        self.Button_Data.append(pygame.image.load(self.file_dir["end"]).convert_alpha()) # TitelScene専用の画像配列
        self.rect_BackGround : pygame.rect.Rect = self.BackGround.get_rect()
        for i in range(len(self.Button_Data)):
             self.rects_Button.append(self.Button_Data[i].get_rect())
             self.time.append(0)
        pygame.mixer.music.load('./Data/sound/title.wav') # BGM読み込み
        pygame.mixer.music.set_volume(self.game_config["SoundVolume"])

    def draw(self):
        if(not pygame.mixer.music.get_busy()) :             #これでBGMがなっているかの判定
                pygame.mixer.music.play(-1)

    def update(self, Screen : pygame.surface.Surface, current_game_scene : dict):
        Screen.fill((255,255,255,))                          # 背景色(ここをうまくやればフェードイン、フェードアウト作れる?)
        Screen.blit(self.BackGround,self.rect_BackGround)

        for i in range(len(self.Button_Data)):
            Screen.blit(self.Button_Data[i], (34 ,382+10*math.sin(math.radians(self.time[i]))+60*i), area=self.rects_Button[i])


        if(MouseClass.MouseClass.isMousePositionChecker(34,382,355,415)):
             if MouseClass.MouseClass.isClickRightButton() : 
                  print("Selected Start Button")
             self.time[0] = (self.time[0] + 1) % (360 * 15)
        elif(MouseClass.MouseClass.isMousePositionChecker(34,442,355,475)):
             if MouseClass.MouseClass.isClickRightButton() : 
                  print("Selected load Button")
             self.time[1] = (self.time[1] + 1) % (360 * 15)
        elif(MouseClass.MouseClass.isMousePositionChecker(34,502,355,535)):
             if MouseClass.MouseClass.isClickRightButton() : 
                  print("Selected Config Button")
             self.time[2] = (self.time[2] + 1) % (360 * 15)
        elif(MouseClass.MouseClass.isMousePositionChecker(34,562,355,595)):
             if MouseClass.MouseClass.isClickRightButton() : 
                  print("Selected end Button")
             self.time[3] = (self.time[3] + 1) % (360 * 15)
        else:
            for i in range(len(self.time)):
             self.time[i] = 0