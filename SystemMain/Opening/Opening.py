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

class OpeningScene(basescene) :
    #def __init__(self, game_config : dict , file_dir : dict, screen : pygame.surface.Surface):
    def __init__(self, gameFandamental : Game_Fandamental, screen : pygame.surface.Surface):
        self.gameFandamental : Game_Fandamental= gameFandamental
        self.Background : BackgroundPicture = BackgroundPicture()
        self.CircleLogo :  MonoPicture = MonoPicture()
        self.Timer : Timer = Timer()

    def initialize(self):
        """    
        picture = pygame.image.load(self.file_dir["CircleLogo"]["Data"]).convert_alpha()
        self.CircleLogo.Regist_order_Picture("CircleLogo", 
                                            picture,
                                            ((self.game_config["WindowWidth"] - picture.get_rect()[2])/2,(self.game_config["WindowHeight"] - picture.get_rect()[3])/2), "IN")
        """
        picture : pygame.surface.Surface = self.gameFandamental.Data["CircleLogo"]["Data"]
        self.CircleLogo.Regist_order_Picture("CircleLogo", 
                                            picture,
                                            ((self.gameFandamental.Config["WindowWidth"] - picture.get_rect()[2])/2,(self.gameFandamental.Config["WindowHeight"] - picture.get_rect()[3])/2), "IN")


        # self.Timer.set_timer(self.file_dir["CircleLogo"]["Display_Time"])
        self.Timer.set_timer(self.gameFandamental.Data["CircleLogo"]["Display_Time"])
        
        self.Timer.timer_start()
        
    def draw(self, Screen :pygame.surface.Surface):
        Screen.fill(color=(255,255,255))
        #self.Background.draw(Screen)
        self.CircleLogo.draw(Screen)


    def update(self, Screen : pygame.surface.Surface, next_game_scene ,  changer, callback_Quit):
        
        for event in pygame.event.get():
            if ((event.type == pygame.MOUSEBUTTONUP) and self.pressedButton[0]):
               changer(CurrentGameScene.CurrentGameScene.TITLE_SCENE)
               return
            elif event.type == QUIT:                          # 終了ボタンを押した場合終了 セーブ警告あり
                if (MessageForeFront("確認", "終了いたしますか。")):
                    callback_Quit(False)
            
            self.pressedButton = pygame.mouse.get_pressed()


        self.Timer.update()
        if(self.Timer.check_time()):
            self.Timer.stop_Timer()
            self.CircleLogo.change_FadeMode("OUT")
        
        if(not(self.Timer.check_start()) and self.CircleLogo.check_Alpha(0)):
            changer(CurrentGameScene.CurrentGameScene.TITLE_SCENE)

        return 
    
    def trans_update(self, Now_game_State:CurrentGameScene.GameState):
        if Now_game_State == CurrentGameScene.GameState.SCENE_FADEIN:
            2+2
        elif Now_game_State == CurrentGameScene.GameState.SCENE_FADEOUT:
            2+2

    """
    def mouse_event(self, pos):
        if(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.file_dir["Title_Scene"]["Start"]["x"],
                                                        self.file_dir["Title_Scene"]["Start"]["y"],
                                                        self.file_dir["Title_Scene"]["Start"]["x"]+self.Button.get_Rect(0,"x"),
                                                        self.file_dir["Title_Scene"]["Start"]["y"]+self.Button.get_Rect(0,"y"))):
            self.BGM.stop_BGM()
            return CurrentGameScene.CurrentGameScene.INTRO
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                          self.file_dir["Title_Scene"]["Load"]["x"],
                                                          self.file_dir["Title_Scene"]["Load"]["y"],
                                                          self.file_dir["Title_Scene"]["Load"]["x"]+self.Button.get_Rect(1,"x"),
                                                          self.file_dir["Title_Scene"]["Load"]["y"]+self.Button.get_Rect(1,"y"))):
            return CurrentGameScene.CurrentGameScene.LOAD
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                          self.file_dir["Title_Scene"]["Config"]["x"],
                                                          self.file_dir["Title_Scene"]["Config"]["y"],
                                                          self.file_dir["Title_Scene"]["Config"]["x"]+self.Button.get_Rect(2,"x"),
                                                          self.file_dir["Title_Scene"]["Config"]["y"]+self.Button.get_Rect(2,"y"))):
            return CurrentGameScene.CurrentGameScene.SETTING
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                          self.file_dir["Title_Scene"]["End"]["x"],
                                                          self.file_dir["Title_Scene"]["End"]["y"],
                                                          self.file_dir["Title_Scene"]["End"]["x"]+self.Button.get_Rect(3,"x"),
                                                          self.file_dir["Title_Scene"]["End"]["y"]+self.Button.get_Rect(3,"y"))):
            return CurrentGameScene.CurrentGameScene.QUIT
        else:
            return CurrentGameScene.CurrentGameScene.NONE_SCENE
        """
    
    def mouse_event(self, pos):
        if(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Title_Scene"]["Start"]["x"],
                                                        self.gameFandamental.Data["Title_Scene"]["Start"]["y"],
                                                        self.gameFandamental.Data["Title_Scene"]["Start"]["x"]+self.Button.get_Rect(0,"x"),
                                                        self.gameFandamental.Data["Title_Scene"]["Start"]["y"]+self.Button.get_Rect(0,"y"))):
            self.BGM.stop_BGM()
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
                                                          self.gameFandamental.Data["Title_Scene"]["End"]["x"],
                                                          self.gameFandamental.Data["Title_Scene"]["End"]["y"],
                                                          self.gameFandamental.Data["Title_Scene"]["End"]["x"]+self.Button.get_Rect(3,"x"),
                                                          self.gameFandamental.Data["Title_Scene"]["End"]["y"]+self.Button.get_Rect(3,"y"))):
            return CurrentGameScene.CurrentGameScene.QUIT
        else:
            return CurrentGameScene.CurrentGameScene.NONE_SCENE