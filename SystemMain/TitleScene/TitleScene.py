import os,sys, random
import tkinter as tki
import tkinter.messagebox as messagebox
import math
import json
import pygame
from pygame.locals import *
from ..MouseClass import MouseClass
import cv2

ROOTPATH = os.path.dirname(os.path.abspath(__file__))
FFGPATH = os.path.dirname(ROOTPATH)
CFGPATH = os.path.dirname(os.path.dirname(ROOTPATH))

class TitleScene :
    def __init__(self, json_data, file_dir):
         self.jd = json_data
         self.fd = file_dir

    def init(self):
        self.time = []
        self.Button_Data = []
        self.rects_Button = []
        #print(self.jd["Title"])
        self.BackGround = pygame.image.load(self.fd["Title"]).convert_alpha() # TitelScene専用の画像配列
        self.Button_Data.append(pygame.image.load(self.fd["Start"]).convert_alpha()) # TitelScene専用の画像配列
        self.Button_Data.append(pygame.image.load(self.fd["load"]).convert_alpha()) # TitelScene専用の画像配列
        self.Button_Data.append(pygame.image.load(self.fd["config"]).convert_alpha()) # TitelScene専用の画像配列
        self.Button_Data.append(pygame.image.load(self.fd["end"]).convert_alpha()) # TitelScene専用の画像配列
        self.rect_BackGround = self.BackGround.get_rect()
        for i in range(len(self.Button_Data)):
             self.rects_Button.append(self.Button_Data[i].get_rect())
             self.time.append(0)
        pygame.mixer.music.load(os.path.normpath(os.path.join(CFGPATH,'Data','sound','title.wav'))) # BGM読み込み
        pygame.mixer.music.set_volume(self.jd["SoundVolume"])
    def draw(self):
        if(not pygame.mixer.music.get_busy()) :             #これでBGMがなっているかの判定
                pygame.mixer.music.play(-1)

        

    def update(self, Screen):
        Screen.fill((255,255,255,))                          # 背景色(ここをうまくやればフェードイン、フェードアウト作れる?)
        Screen.blit(self.BackGround,self.rect_BackGround)

        for i in range(len(self.Button_Data)):
            Screen.blit(self.Button_Data[i], (34 ,382+10*math.sin(math.radians(self.time[i]))+60*i), area=self.rects_Button[i])


        if(MouseClass.MouseClass.isMousePositionChecker(34,382,355,415)):
             if MouseClass.MouseClass.isClickRightButton() : 
                  print("Selected Start Button")
             self.time[0] = (self.time[0] + 1) % 360
        elif(MouseClass.MouseClass.isMousePositionChecker(34,442,355,475)):
             if MouseClass.MouseClass.isClickRightButton() : 
                  print("Selected load Button")
             self.time[1] = (self.time[1] + 1) % 360
        elif(MouseClass.MouseClass.isMousePositionChecker(34,502,355,535)):
             if MouseClass.MouseClass.isClickRightButton() : 
                  print("Selected Config Button")
             self.time[2] = (self.time[2] + 1) % 360
        elif(MouseClass.MouseClass.isMousePositionChecker(34,562,355,595)):
             if MouseClass.MouseClass.isClickRightButton() : 
                  print("Selected end Button")
             self.time[3] = (self.time[3] + 1) % 360
        else:
            for i in range(len(self.time)):
             self.time[i] = 0