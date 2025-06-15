import os
import pygame
from enum import Enum
from pygame.locals import *
from SystemMain.MouseClass import MouseClass
from SystemMain.BaseClass import basescene
from SystemMain.GameScene import GameScene,CurrentGameScene
from SystemMain.LoadScene import LoadScene
from SystemMain.SystemLib import *


ROOTPATH = os.path.dirname(os.path.abspath(__file__))
FFGPATH = os.path.dirname(ROOTPATH)
CFGPATH = os.path.dirname(os.path.dirname(ROOTPATH))

class GalleryScene(basescene) :
    #def __init__(self, game_config : dict , file_dir : dict, screen : pygame.surface.Surface):
    def __init__(self, gameFandamental : Game_Fandamental, screen : pygame.surface.Surface):
        #self.game_config : dict = game_config
        #self.file_dir : dict = file_dir
        self.gameFandamental : Game_Fandamental = gameFandamental
        self.Background : BackgroundPicture = BackgroundPicture()
        self.onCursol : MonoPicture = MonoPicture()
        self.isOnCursol : bool = False
        self.Button : MonoPicture = MonoPicture()
        self.BGM : GameSound = GameSound(self.gameFandamental)
        self.pressedButton = (False,False,False) # ボタン押し状態
        self.isDrawCG : bool = False
        self.CG : MonoPicture = MonoPicture()

    def initialize(self):
        self.Background.Regist_order_Picture("Gallery", 
                                             pygame.transform.scale(self.gameFandamental.Data["Gallery"]["BackGround"]["Data"], 
                                                                    (self.gameFandamental.Config["WindowWidth"],self.gameFandamental.Config["WindowHeight"])), 
                                             (0,0))
        self.onCursol.Regist_order_Picture("OverPict", 
                                            self.gameFandamental.Data["Gallery"]["OverPict"]["Data"], 
                                            (self.gameFandamental.Data["Gallery"]["CG1"]["x"],self.gameFandamental.Data["Gallery"]["CG1"]["y"]))
        self.Button.Regist_order_Picture("Return", 
                                            self.gameFandamental.Data["Gallery"]["Return"]["Data"], 
                                            (self.gameFandamental.Data["Gallery"]["Return"]["x"],self.gameFandamental.Data["Gallery"]["Return"]["y"]))
        self.CG.Regist_order_Picture("CG",
                                    pygame.transform.scale(self.gameFandamental.Data["Story"]["Picture"]["black"], 
                                        (self.gameFandamental.Config["WindowWidth"],self.gameFandamental.Config["WindowHeight"])), 
                                        (0,0))

    def draw(self, Screen :pygame.surface.Surface):
        self.Background.draw(Screen)

        if self.isOnCursol:
            self.onCursol.draw(Screen)

        self.Button.draw(Screen)

        if self.isDrawCG:
            self.CG.draw(Screen)

    def update(self, Screen : pygame.surface.Surface, next_game_scene ,  changer, callback_Quit):
        
        pos = pygame.mouse.get_pos
        for event in pygame.event.get():
            if ((event.type == pygame.MOUSEBUTTONUP) and self.pressedButton[0] and not(self.isDrawCG)):
                gamescene = self.mouse_event(pos)
                if (gamescene == CurrentGameScene.CurrentGameScene.RETURN):
                    changer(gamescene)
                elif ('CG' in gamescene.name):
                    self.CG.Regist_order_Picture("CG",
                                                pygame.transform.scale(self.gameFandamental.Data["Story"]["Picture"][gamescene.name.lower()], 
                                                                    (self.gameFandamental.Config["WindowWidth"],self.gameFandamental.Config["WindowHeight"])), 
                                             (0,0), "IN")
                    self.isDrawCG = True
                return
            elif((event.type == pygame.MOUSEBUTTONUP) and self.pressedButton[0] and self.isDrawCG):
                self.CG.change_FadeMode("OUT")
            elif event.type == QUIT:                          # 終了ボタンを押した場合終了 セーブ警告あり
                if (MessageForeFront("確認", "終了いたしますか。")):
                    if(os.path.isfile("./Data/save/tmp.png")):
                        os.remove("./Data/save/tmp.png")
                    callback_Quit(False)

            self.pressedButton = pygame.mouse.get_pressed()
        
        if self.CG.check_Alpha(0):
            self.isDrawCG = False

        NowPos = self.mouse_event(pos)
        if ('CG' in NowPos.name):
            self.change_CG(NowPos.name,True)
        else:
            self.change_CG(NowPos.name)
        return 
    
    def mouse_event(self, pos):
        if(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Gallery"]["Return"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["Return"]["y"],
                                                        self.gameFandamental.Data["Gallery"]["Return"]["x"]+self.Button.get_rect(0),
                                                        self.gameFandamental.Data["Gallery"]["Return"]["y"]+self.Button.get_rect(1))):
            return CurrentGameScene.CurrentGameScene.RETURN
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Gallery"]["CG1"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG1"]["y"],
                                                        self.gameFandamental.Data["Gallery"]["CG1"]["x"]+self.gameFandamental.Data["Gallery"]["CGSize"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG1"]["y"]+self.gameFandamental.Data["Gallery"]["CGSize"]["y"])):
            return CurrentGameScene.CurrentGameScene.CG1
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Gallery"]["CG201"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG201"]["y"],
                                                        self.gameFandamental.Data["Gallery"]["CG201"]["x"]+self.gameFandamental.Data["Gallery"]["CGSize"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG201"]["y"]+self.gameFandamental.Data["Gallery"]["CGSize"]["y"])):
            return CurrentGameScene.CurrentGameScene.CG201
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Gallery"]["CG202"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG202"]["y"],
                                                        self.gameFandamental.Data["Gallery"]["CG202"]["x"]+self.gameFandamental.Data["Gallery"]["CGSize"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG202"]["y"]+self.gameFandamental.Data["Gallery"]["CGSize"]["y"])):
            return CurrentGameScene.CurrentGameScene.CG202
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Gallery"]["CG3"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG3"]["y"],
                                                        self.gameFandamental.Data["Gallery"]["CG3"]["x"]+self.gameFandamental.Data["Gallery"]["CGSize"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG3"]["y"]+self.gameFandamental.Data["Gallery"]["CGSize"]["y"])):
            return CurrentGameScene.CurrentGameScene.CG3
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Gallery"]["CG4"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG4"]["y"],
                                                        self.gameFandamental.Data["Gallery"]["CG4"]["x"]+self.gameFandamental.Data["Gallery"]["CGSize"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG4"]["y"]+self.gameFandamental.Data["Gallery"]["CGSize"]["y"])):
            return CurrentGameScene.CurrentGameScene.CG4
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Gallery"]["CG5"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG5"]["y"],
                                                        self.gameFandamental.Data["Gallery"]["CG5"]["x"]+self.gameFandamental.Data["Gallery"]["CGSize"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG5"]["y"]+self.gameFandamental.Data["Gallery"]["CGSize"]["y"])):
            return CurrentGameScene.CurrentGameScene.CG5
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Gallery"]["CG6"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG6"]["y"],
                                                        self.gameFandamental.Data["Gallery"]["CG6"]["x"]+self.gameFandamental.Data["Gallery"]["CGSize"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG6"]["y"]+self.gameFandamental.Data["Gallery"]["CGSize"]["y"])):
            return CurrentGameScene.CurrentGameScene.CG6
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Gallery"]["CG7"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG7"]["y"],
                                                        self.gameFandamental.Data["Gallery"]["CG7"]["x"]+self.gameFandamental.Data["Gallery"]["CGSize"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG7"]["y"]+self.gameFandamental.Data["Gallery"]["CGSize"]["y"])):
            return CurrentGameScene.CurrentGameScene.CG7
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Gallery"]["CG8"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG8"]["y"],
                                                        self.gameFandamental.Data["Gallery"]["CG8"]["x"]+self.gameFandamental.Data["Gallery"]["CGSize"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG8"]["y"]+self.gameFandamental.Data["Gallery"]["CGSize"]["y"])):
            return CurrentGameScene.CurrentGameScene.CG8
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Gallery"]["CG10"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG10"]["y"],
                                                        self.gameFandamental.Data["Gallery"]["CG10"]["x"]+self.gameFandamental.Data["Gallery"]["CGSize"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG10"]["y"]+self.gameFandamental.Data["Gallery"]["CGSize"]["y"])):
            return CurrentGameScene.CurrentGameScene.CG10
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Gallery"]["CG11"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG11"]["y"],
                                                        self.gameFandamental.Data["Gallery"]["CG11"]["x"]+self.gameFandamental.Data["Gallery"]["CGSize"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG11"]["y"]+self.gameFandamental.Data["Gallery"]["CGSize"]["y"])):
            return CurrentGameScene.CurrentGameScene.CG11
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Gallery"]["CG12"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG12"]["y"],
                                                        self.gameFandamental.Data["Gallery"]["CG12"]["x"]+self.gameFandamental.Data["Gallery"]["CGSize"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG12"]["y"]+self.gameFandamental.Data["Gallery"]["CGSize"]["y"])):
            return CurrentGameScene.CurrentGameScene.CG12
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Gallery"]["CG13"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG13"]["y"],
                                                        self.gameFandamental.Data["Gallery"]["CG13"]["x"]+self.gameFandamental.Data["Gallery"]["CGSize"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG13"]["y"]+self.gameFandamental.Data["Gallery"]["CGSize"]["y"])):
            return CurrentGameScene.CurrentGameScene.CG13
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Gallery"]["CG14"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG14"]["y"],
                                                        self.gameFandamental.Data["Gallery"]["CG14"]["x"]+self.gameFandamental.Data["Gallery"]["CGSize"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG14"]["y"]+self.gameFandamental.Data["Gallery"]["CGSize"]["y"])):
            return CurrentGameScene.CurrentGameScene.CG14
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Gallery"]["CG15"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG15"]["y"],
                                                        self.gameFandamental.Data["Gallery"]["CG15"]["x"]+self.gameFandamental.Data["Gallery"]["CGSize"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG15"]["y"]+self.gameFandamental.Data["Gallery"]["CGSize"]["y"])):
            return CurrentGameScene.CurrentGameScene.CG15
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Gallery"]["CG16"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG16"]["y"],
                                                        self.gameFandamental.Data["Gallery"]["CG16"]["x"]+self.gameFandamental.Data["Gallery"]["CGSize"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG16"]["y"]+self.gameFandamental.Data["Gallery"]["CGSize"]["y"])):
            return CurrentGameScene.CurrentGameScene.CG16
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Gallery"]["CG17"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG17"]["y"],
                                                        self.gameFandamental.Data["Gallery"]["CG17"]["x"]+self.gameFandamental.Data["Gallery"]["CGSize"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG17"]["y"]+self.gameFandamental.Data["Gallery"]["CGSize"]["y"])):
            return CurrentGameScene.CurrentGameScene.CG17
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Gallery"]["CG18"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG18"]["y"],
                                                        self.gameFandamental.Data["Gallery"]["CG18"]["x"]+self.gameFandamental.Data["Gallery"]["CGSize"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG18"]["y"]+self.gameFandamental.Data["Gallery"]["CGSize"]["y"])):
            return CurrentGameScene.CurrentGameScene.CG18
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Gallery"]["CG19"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG19"]["y"],
                                                        self.gameFandamental.Data["Gallery"]["CG19"]["x"]+self.gameFandamental.Data["Gallery"]["CGSize"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG19"]["y"]+self.gameFandamental.Data["Gallery"]["CGSize"]["y"])):
            return CurrentGameScene.CurrentGameScene.CG19
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Gallery"]["CG20"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG20"]["y"],
                                                        self.gameFandamental.Data["Gallery"]["CG20"]["x"]+self.gameFandamental.Data["Gallery"]["CGSize"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG20"]["y"]+self.gameFandamental.Data["Gallery"]["CGSize"]["y"])):
            return CurrentGameScene.CurrentGameScene.CG20
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Gallery"]["CG21"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG21"]["y"],
                                                        self.gameFandamental.Data["Gallery"]["CG21"]["x"]+self.gameFandamental.Data["Gallery"]["CGSize"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG21"]["y"]+self.gameFandamental.Data["Gallery"]["CGSize"]["y"])):
            return CurrentGameScene.CurrentGameScene.CG21
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Gallery"]["CG22"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG22"]["y"],
                                                        self.gameFandamental.Data["Gallery"]["CG22"]["x"]+self.gameFandamental.Data["Gallery"]["CGSize"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG22"]["y"]+self.gameFandamental.Data["Gallery"]["CGSize"]["y"])):
            return CurrentGameScene.CurrentGameScene.CG22
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Gallery"]["CG23"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG23"]["y"],
                                                        self.gameFandamental.Data["Gallery"]["CG23"]["x"]+self.gameFandamental.Data["Gallery"]["CGSize"]["x"],
                                                        self.gameFandamental.Data["Gallery"]["CG23"]["y"]+self.gameFandamental.Data["Gallery"]["CGSize"]["y"])):
            return CurrentGameScene.CurrentGameScene.CG23
        else:
            return CurrentGameScene.CurrentGameScene.NONE_SCENE
        """elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                self.file_dir["Gallery"]["CG9"]["x"],
                                                self.file_dir["Gallery"]["CG9"]["y"],
                                                self.file_dir["Gallery"]["CG9"]["x"]+self.file_dir["Gallery"]["CGSize"]["x"],
                                                self.file_dir["Gallery"]["CG9"]["y"]+self.file_dir["Gallery"]["CGSize"]["y"])):
            return CurrentGameScene.CurrentGameScene.CG9"""
    
    def change_CG(self, EnumName : str , value : bool = False):
        if('CG' in EnumName):
            self.onCursol.change_Coordinate((self.gameFandamental.Data["Gallery"][EnumName]["x"],self.gameFandamental.Data["Gallery"][EnumName]["y"]))

        self.isOnCursol = value