import os,sys, random
import json
import pygame
from pygame.locals import *
from ..MouseClass import MouseClass
import cv2

ROOTPATH = os.path.dirname(os.path.abspath(__file__))
FFGPATH = os.path.dirname(ROOTPATH)
CFGPATH = os.path.dirname(os.path.dirname(ROOTPATH))

class TitleScene :
    def init(self,json_data):
        self.TitlePicture = pygame.image.load(os.path.normpath(os.path.join(CFGPATH,'Data','image','menu.png'))).convert_alpha() # TitelScene専用の画像配列
        self.rect_TitlePicture = self.TitlePicture.get_rect()
        pygame.mixer.music.load(os.path.normpath(os.path.join(CFGPATH,'Data','sound','title.wav'))) # BGM読み込み
        pygame.mixer.music.set_volume(json_data["SoundVolume"])

    def draw(self,Screen):

        if(not pygame.mixer.music.get_busy()) :             #これでBGMがなっているかの判定
                pygame.mixer.music.play(-1)
        Screen.fill((0,0,0,))                          # 背景色(ここをうまくやればフェードイン、フェードアウト作れる?)
        Screen.blit(self.TitlePicture,self.rect_TitlePicture)
        
        pygame.display.update()
    def update():
        return
    