import os
import pygame
from pygame.locals import *
from SystemMain.MouseClass import MouseClass
from SystemMain.BaseClass import basescene
from SystemMain.GameScene import GameScene,CurrentGameScene
from SystemMain.LoadScene import LoadScene
from SystemMain.SystemLib import *

ROOTPATH = os.path.dirname(os.path.abspath(__file__))
FFGPATH = os.path.dirname(ROOTPATH)
CFGPATH = os.path.dirname(os.path.dirname(ROOTPATH))

class TitleScene(basescene) :
    
    # def __init__(self, game_config : dict , file_dir : dict, screen : pygame.surface.Surface):
    def __init__(self, gameFandamental : Game_Fandamental, screen : pygame.surface.Surface):
        
        self.gameFandamental : Game_Fandamental = gameFandamental
        self.Background : BackgroundPicture = BackgroundPicture()
        self.TitleLogo :  MonoPicture = MonoPicture()
        self.Button : Multiple_Picture = Multiple_Picture()
        self.omake : MonoPicture = MonoPicture()
        self.BGM : GameSound = GameSound(self.gameFandamental)
        self.pressedButton = (False,False,False) # ボタン押し状態

    def initialize(self):
        self.Background.Regist_order_Picture("TitleScene", 
                                             pygame.transform.scale(self.gameFandamental.Data["Title_Scene"]["Title"][str(self.gameFandamental.Config["Cleared"])]["Data"], 
                                                                    (self.gameFandamental.Config["WindowWidth"],self.gameFandamental.Config["WindowHeight"])), 
                                             (0,0))
        self.TitleLogo.Regist_order_Picture("TitleLogo", 
                                            self.gameFandamental.Data["Title_Scene"]["TitleName"]["Data"], 
                                            (self.gameFandamental.Data["Title_Scene"]["TitleName"]["x"],self.gameFandamental.Data["Title_Scene"]["TitleName"]["y"]), "Normal")

        self.gameFandamental.Data["tmp_Save"]["Scene_ID"] = -1
        self.gameFandamental.Data["tmp_Save"]["BackGround"]["Data"] = "Data/image/back/black.jpg"
        self.gameFandamental.Data["tmp_Save"]["BackGround"]["Name"] = "Black"
        self.gameFandamental.Data["tmp_Save"]["BGM"] = ""

        for data in ["Start", "Load", "Config", "End"]:
            self.Button.Regist_Pictures(data, 
                                        self.gameFandamental.Data["Title_Scene"][data]["0"]["Data"], 
                                        (self.gameFandamental.Data["Title_Scene"][data]["x"] ,self.gameFandamental.Data["Title_Scene"][data]["y"]),
                                        "Normal")
            
        self.omake.Regist_order_Picture("Gallery",
                                        self.gameFandamental.Data["Title_Scene"]["Gallery"]["0"]["Data"],
                                        (self.gameFandamental.Data["Title_Scene"]["Gallery"]["x"] ,self.gameFandamental.Data["Title_Scene"]["Gallery"]["y"]),
                                        "Normal")
        
        if(self.BGM.busy()):
            self.BGM.stop_BGM()

        self.BGM.start_BGM(self.gameFandamental.Data["Title_Scene"]["BGM"])

    def draw(self, Screen :pygame.surface.Surface):
        self.Background.draw(Screen)
        self.TitleLogo.draw(Screen)
        self.Button.draw(Screen)

        if(self.gameFandamental.Config["Cleared"]):
            self.omake.draw(Screen)

    def update(self, Screen : pygame.surface.Surface, next_game_scene ,  changer, callback_Quit):
        
        for event in pygame.event.get():
            if ((event.type == pygame.MOUSEBUTTONUP) and self.pressedButton[0]):
               changer(self.mouse_event(pygame.mouse.get_pos))
               return
            elif event.type == QUIT:                          # 終了ボタンを押した場合終了 セーブ警告あり
                if (MessageForeFront("確認", "終了いたしますか。")):
                    if(os.path.isfile("./Data/save/tmp.png")):
                        os.remove("./Data/save/tmp.png")
                    callback_Quit(False)

            self.pressedButton = pygame.mouse.get_pressed()

        self.transPosition(pygame.mouse.get_pos)
        return 

    def mouse_event(self, pos):
        if(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Title_Scene"]["Start"]["x"],
                                                        self.gameFandamental.Data["Title_Scene"]["Start"]["y"],
                                                        self.gameFandamental.Data["Title_Scene"]["Start"]["x"]+self.Button.get_Rect(0,"x"),
                                                        self.gameFandamental.Data["Title_Scene"]["Start"]["y"]+self.Button.get_Rect(0,"y"))):
            return CurrentGameScene.CurrentGameScene.INTRO
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                          self.gameFandamental.Data["Title_Scene"]["Load"]["x"],
                                                          self.gameFandamental.Data["Title_Scene"]["Load"]["y"],
                                                          self.gameFandamental.Data["Title_Scene"]["Load"]["x"]+self.Button.get_Rect(1,"x"),
                                                          self.gameFandamental.Data["Title_Scene"]["Load"]["y"]+self.Button.get_Rect(1,"y"))):
            return CurrentGameScene.CurrentGameScene.LOAD
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                          self.gameFandamental.Data["Title_Scene"]["Config"]["x"],
                                                          self.gameFandamental.Data["Title_Scene"]["Config"]["y"],
                                                          self.gameFandamental.Data["Title_Scene"]["Config"]["x"]+self.Button.get_Rect(2,"x"),
                                                          self.gameFandamental.Data["Title_Scene"]["Config"]["y"]+self.Button.get_Rect(2,"y"))):
            return CurrentGameScene.CurrentGameScene.SETTING
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                          self.gameFandamental.Data["Title_Scene"]["Gallery"]["x"],
                                                          self.gameFandamental.Data["Title_Scene"]["Gallery"]["y"],
                                                          self.gameFandamental.Data["Title_Scene"]["Gallery"]["x"]+self.omake.get_rect(0),
                                                          self.gameFandamental.Data["Title_Scene"]["Gallery"]["y"]+self.omake.get_rect(1)) and self.gameFandamental.Config["Cleared"] == 1):
            return CurrentGameScene.CurrentGameScene.GALLERY
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                          self.gameFandamental.Data["Title_Scene"]["End"]["x"],
                                                          self.gameFandamental.Data["Title_Scene"]["End"]["y"],
                                                          self.gameFandamental.Data["Title_Scene"]["End"]["x"]+self.Button.get_Rect(3,"x"),
                                                          self.gameFandamental.Data["Title_Scene"]["End"]["y"]+self.Button.get_Rect(3,"y"))):
            return CurrentGameScene.CurrentGameScene.QUIT
        else:
            return CurrentGameScene.CurrentGameScene.NONE_SCENE
        
    def transPosition(self, pos):

        if(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Title_Scene"]["Start"]["x"],
                                                        self.gameFandamental.Data["Title_Scene"]["Start"]["y"],
                                                        self.gameFandamental.Data["Title_Scene"]["Start"]["x"]+self.Button.get_Rect(0,"x"),
                                                        self.gameFandamental.Data["Title_Scene"]["Start"]["y"]+self.Button.get_Rect(0,"y"))):
            self.Button.change_Picture("Start", self.gameFandamental.Data["Title_Scene"]["Start"]["1"]["Data"], 0)
            return
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                          self.gameFandamental.Data["Title_Scene"]["Load"]["x"],
                                                          self.gameFandamental.Data["Title_Scene"]["Load"]["y"],
                                                          self.gameFandamental.Data["Title_Scene"]["Load"]["x"]+self.Button.get_Rect(1,"x"),
                                                          self.gameFandamental.Data["Title_Scene"]["Load"]["y"]+self.Button.get_Rect(1,"y"))):
            self.Button.change_Picture("Load", self.gameFandamental.Data["Title_Scene"]["Load"]["1"]["Data"], 1)
            return
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                          self.gameFandamental.Data["Title_Scene"]["Config"]["x"],
                                                          self.gameFandamental.Data["Title_Scene"]["Config"]["y"],
                                                          self.gameFandamental.Data["Title_Scene"]["Config"]["x"]+self.Button.get_Rect(2,"x"),
                                                          self.gameFandamental.Data["Title_Scene"]["Config"]["y"]+self.Button.get_Rect(2,"y"))):
            self.Button.change_Picture("Config", self.gameFandamental.Data["Title_Scene"]["Config"]["1"]["Data"], 2)
            return
        if(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                          self.gameFandamental.Data["Title_Scene"]["Gallery"]["x"],
                                                          self.gameFandamental.Data["Title_Scene"]["Gallery"]["y"],
                                                          self.gameFandamental.Data["Title_Scene"]["Gallery"]["x"]+self.omake.get_rect(0),
                                                          self.gameFandamental.Data["Title_Scene"]["Gallery"]["y"]+self.omake.get_rect(1)) and self.gameFandamental.Config["Cleared"] == 1):
            self.omake.Regist_order_Picture("Gallery",
                                        self.gameFandamental.Data["Title_Scene"]["Gallery"]["1"]["Data"],
                                        (self.gameFandamental.Data["Title_Scene"]["Gallery"]["x"] ,self.gameFandamental.Data["Title_Scene"]["Gallery"]["y"]),
                                        "Normal")
            return
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                          self.gameFandamental.Data["Title_Scene"]["End"]["x"],
                                                          self.gameFandamental.Data["Title_Scene"]["End"]["y"],
                                                          self.gameFandamental.Data["Title_Scene"]["End"]["x"]+self.Button.get_Rect(3,"x"),
                                                          self.gameFandamental.Data["Title_Scene"]["End"]["y"]+self.Button.get_Rect(3,"y"))):
            self.Button.change_Picture("End", self.gameFandamental.Data["Title_Scene"]["End"]["1"]["Data"], 3)
            return
        else:
            self.Button.change_Picture("Start", self.gameFandamental.Data["Title_Scene"]["Start"]["0"]["Data"], 0)
            self.Button.change_Picture("Load", self.gameFandamental.Data["Title_Scene"]["Load"]["0"]["Data"], 1)
            self.Button.change_Picture("Config", self.gameFandamental.Data["Title_Scene"]["Config"]["0"]["Data"], 2)
            self.Button.change_Picture("End", self.gameFandamental.Data["Title_Scene"]["End"]["0"]["Data"], 3)

            if(self.gameFandamental.Config["Cleared"] == 1):
                self.omake.Regist_order_Picture("Gallery",
                                        self.gameFandamental.Data["Title_Scene"]["Gallery"]["0"]["Data"],
                                        (self.gameFandamental.Data["Title_Scene"]["Gallery"]["x"] ,self.gameFandamental.Data["Title_Scene"]["Gallery"]["y"]),
                                        "Normal")

            return
