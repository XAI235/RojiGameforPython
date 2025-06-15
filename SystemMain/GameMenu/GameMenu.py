import os
import json
import tempfile
import pygame
from pygame.locals import *
from SystemMain.TitleScene import TitleScene
from SystemMain.GameScene import GameScene, CurrentGameScene
from SystemMain.LoadScene import LoadScene
from SystemMain.BaseClass import basescene
from SystemMain.Stack import stack
from SystemMain.SystemLib import *


class GameMenu(basescene) : 
    # def __init__(self, game_config : dict , file_dir : dict):
    def __init__(self, gameFandamental : Game_Fandamental):
        #self.game_config : dict = game_config
        #self.file_dir : dict = file_dir
        self.gameFandamental : Game_Fandamental = gameFandamental

        self.next_scene : CurrentGameScene.NextGameOperation = CurrentGameScene.NextGameOperation.NONE

        self.MenuDisplay : BackgroundPicture = BackgroundPicture()
        self.FSButton : MonoPicture = MonoPicture()
        self.WdwButton : MonoPicture = MonoPicture()
        self.NWButton : MonoPicture = MonoPicture()
        self.FstButton : MonoPicture = MonoPicture()
        self.NrlButton : MonoPicture = MonoPicture()
        self.SlwButton : MonoPicture = MonoPicture()
        self.SvButton : MonoPicture = MonoPicture()
        self.LdButton : MonoPicture = MonoPicture()
        self.TtlButton : MonoPicture = MonoPicture()
        self.RtnButton : MonoPicture = MonoPicture()

        self.translucent_bou : MonoPicture = MonoPicture()

        self.MenuFullScreen : MonoPicture = MonoPicture()
        self.MenuAutomaticRead : MonoPicture = MonoPicture()
        self.MenuSoundVolume : MonoPicture = MonoPicture()
        self.MenuVoiceVolume : MonoPicture = MonoPicture()
        self.BGM : GameSound = GameSound(gameFandamental)
        return
    
    def initialize(self):
        self.MenuDisplay.Regist_order_Picture("Background",
                                              pygame.transform.scale(self.gameFandamental.Data["Setting"]["BackGround"]["Data"],
                                                                    (self.gameFandamental.Config["WindowWidth"],self.gameFandamental.Config["WindowHeight"])),
                                                                     (self.gameFandamental.Data["Setting"]["BackGround"]["x"],self.gameFandamental.Data["Setting"]["BackGround"]["y"]))
                                                                     
        self.FSButton.Regist_order_Picture("FullScreen",
                                           self.gameFandamental.Data["Setting"]["Full"]["Pict"]["Data"],
                                           (self.gameFandamental.Data["Setting"]["Full"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Full"]["Pict"]["y"]))
        self.WdwButton.Regist_order_Picture("Window",
                                            self.gameFandamental.Data["Setting"]["Window"]["Pict"]["Data"],
                                            (self.gameFandamental.Data["Setting"]["Window"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Window"]["Pict"]["y"]))
        
        self.NWButton.Regist_order_Picture("NoWait",
                                           self.gameFandamental.Data["Setting"]["noWait"]["Pict"]["Data"],
                                           (self.gameFandamental.Data["Setting"]["noWait"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["noWait"]["Pict"]["y"]))
        
        self.FstButton.Regist_order_Picture("Fast",
                                            self.gameFandamental.Data["Setting"]["Fast"]["Pict"]["Data"],
                                            (self.gameFandamental.Data["Setting"]["Fast"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Fast"]["Pict"]["y"]))
        
        self.NrlButton.Regist_order_Picture("Normal",
                                            self.gameFandamental.Data["Setting"]["Normal"]["Pict"]["Data"],
                                            (self.gameFandamental.Data["Setting"]["Normal"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Normal"]["Pict"]["y"]))
        
        self.SlwButton.Regist_order_Picture("Slow",
                                            self.gameFandamental.Data["Setting"]["Slow"]["Pict"]["Data"],
                                            (self.gameFandamental.Data["Setting"]["Slow"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Slow"]["Pict"]["y"]))
        
        self.SvButton.Regist_order_Picture("Save",
                                           self.gameFandamental.Data["Setting"]["Save"]["Pict"]["Data"],
                                           (self.gameFandamental.Data["Setting"]["Save"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Save"]["Pict"]["y"]))
        
        self.LdButton.Regist_order_Picture("Load",
                                           self.gameFandamental.Data["Setting"]["Load"]["Pict"]["Data"],
                                           (self.gameFandamental.Data["Setting"]["Load"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Load"]["Pict"]["y"]))
        
        self.TtlButton.Regist_order_Picture("Title",
                                            self.gameFandamental.Data["Setting"]["Title"]["Pict"]["Data"],
                                            (self.gameFandamental.Data["Setting"]["Title"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Title"]["Pict"]["y"]))
        
        self.RtnButton.Regist_order_Picture("Return",
                                            self.gameFandamental.Data["Setting"]["Return"]["Pict"]["Data"],
                                            (self.gameFandamental.Data["Setting"]["Return"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Return"]["Pict"]["y"]))

        self.translucent_bou.Regist_order_Picture("translucent",
                                                  self.gameFandamental.Data["Setting"]["Translusent"]["Data"],(0,0))


        self.MenuFullScreen.Regist_order_Picture("bou", 
                                                 self.gameFandamental.Data["Setting"]["bou"]["Data"], 
                                                 (self.gameFandamental.Data["Setting"][self.gameFandamental.Config["WindowMode"]]["x"],self.gameFandamental.Data["Setting"][self.gameFandamental.Config["WindowMode"]]["y"]))
        
        self.MenuAutomaticRead.Regist_order_Picture("bou", 
                                                    self.gameFandamental.Data["Setting"]["bou"]["Data"], 
                                                    (self.gameFandamental.Data["Setting"][self.gameFandamental.Config["Automatic_Character_Feed"]]["x"],self.gameFandamental.Data["Setting"][self.gameFandamental.Config["Automatic_Character_Feed"]]["y"]))
        
        self.MenuSoundVolume.Regist_order_Picture("maru", 
                                                  self.gameFandamental.Data["Setting"]
                                                  ["maru"]["Data"], 
                                                  (self.gameFandamental.Data["Setting"]["Sound"][self.gameFandamental.Config["SoundVolume"]]["x"],self.gameFandamental.Data["Setting"]["Sound"][self.gameFandamental.Config["SoundVolume"]]["y"]))
        
        self.MenuVoiceVolume.Regist_order_Picture("maru", 
                                                  self.gameFandamental.Data["Setting"]["maru"]["Data"], 
                                                  (self.gameFandamental.Data["Setting"]["Voice"][self.gameFandamental.Config["VoiceVolume"]]["x"],self.gameFandamental.Data["Setting"]["Voice"][self.gameFandamental.Config["VoiceVolume"]]["y"]))
        return 
    
    def update(self, Screen : pygame.surface.Surface, next_game_scene ,  changer, callback_Quit):
        
        for event in pygame.event.get():
            button = pygame.mouse.get_pressed()
            if(((event.type == pygame.MOUSEBUTTONUP) and self.pressedButton[0])):
                self.next_scene = self.mouse_event(pygame.mouse.get_pos)
                if(self.next_scene == CurrentGameScene.NextGameOperation.RETURNTOPREVIEW):
                   self.Saveing_Setting()
                   changer(CurrentGameScene.CurrentGameScene.RETURN)
                elif(self.next_scene == CurrentGameScene.NextGameOperation.GOTOTitle):        
                    self.gameFandamental.Data["tmp_Save"]["Scene_ID"] = -1
                    self.Saveing_Setting()
                    changer(CurrentGameScene.CurrentGameScene.TITLE_SCENE)
                elif(self.next_scene == CurrentGameScene.NextGameOperation.GOTOSAVE):
                    if(self.gameFandamental.Data["tmp_Save"]["Scene_ID"] >= 0 ):    
                        changer(CurrentGameScene.CurrentGameScene.SAVE)
                elif(self.next_scene == CurrentGameScene.NextGameOperation.GOTOLOAD):
                    if(self.gameFandamental.Data["tmp_Save"]["Scene_ID"] >= 0 ):
                        changer(CurrentGameScene.CurrentGameScene.LOAD)
                elif(self.next_scene == CurrentGameScene.NextGameOperation.CHENGEDISPLAY):
                    self.MenuFullScreen.change_Coordinate((self.gameFandamental.Data["Setting"][self.gameFandamental.Config["WindowMode"]]["x"],self.gameFandamental.Data["Setting"][self.gameFandamental.Config["WindowMode"]]["y"]))
                    if self.gameFandamental.Config["WindowMode"] == "Window":
                        pygame.display.set_mode((self.gameFandamental.Config["WindowWidth"],
                                                self.gameFandamental.Config["WindowHeight"]), pygame.SCALED)  # 画面サイズ設定
                    elif self.gameFandamental.Config["WindowMode"] == "Full":
                        pygame.display.set_mode((self.gameFandamental.Config["WindowWidth"], 
                                                               self.gameFandamental.Config["WindowHeight"]), pygame.FULLSCREEN | pygame.SCALED)  # 画面サイズ設定
                elif(self.next_scene == CurrentGameScene.NextGameOperation.CHENGEAUTO):    
                    self.MenuAutomaticRead.change_Coordinate((self.gameFandamental.Data["Setting"][self.gameFandamental.Config["Automatic_Character_Feed"]]["x"],self.gameFandamental.Data["Setting"][self.gameFandamental.Config["Automatic_Character_Feed"]]["y"]))
                elif(self.next_scene == CurrentGameScene.NextGameOperation.CHENGEVOICE):
                    self.MenuVoiceVolume.change_Coordinate((self.gameFandamental.Data["Setting"]["Voice"][self.gameFandamental.Config["VoiceVolume"]]["x"],self.gameFandamental.Data["Setting"]["Voice"][self.gameFandamental.Config["VoiceVolume"]]["y"]))
                    self.BGM.update_Volume()
                elif(self.next_scene == CurrentGameScene.NextGameOperation.CHENGESOUND):
                    self.MenuSoundVolume.change_Coordinate((self.gameFandamental.Data["Setting"]["Sound"][self.gameFandamental.Config["SoundVolume"]]["x"],self.gameFandamental.Data["Setting"]["Sound"][self.gameFandamental.Config["SoundVolume"]]["y"]))
                    self.BGM.update_Volume()
                elif(self.next_scene == CurrentGameScene.NextGameOperation.CHENGEDISPLAY):
                    self.MenuVoiceVolume.change_Coordinate((self.gameFandamental.Data["Setting"]["Voice"][self.gameFandamental.Config["VoiceVolume"]]["x"],self.gameFandamental.Data["Setting"]["Voice"][self.gameFandamental.Config["VoiceVolume"]]["y"]))
                    self.BGM.update_Volume()
                    
                return
            elif event.type == QUIT:                          # 終了ボタンを押した場合終了 セーブ警告あり
                callback_Quit(not(MessageForeFront("確認", "終了いたしますか。")))
                #callback_Quit(not(messagebox.askyesno("確認", "終了いたしますか。")))

            self.set_translucentPosition(pygame.mouse.get_pos)
            self.pressedButton = pygame.mouse.get_pressed() # ここでマウスの状態を保存しているはず…。
        
        return
    
    def draw(self, Screen :pygame.surface.Surface):
        #Screen.blit(self.MenuDisplay, dest=(0,0), area=self.MenuDisplay.get_rect())
        self.MenuDisplay.draw(Screen)
        
        # ウィンドウサイズ
        self.FSButton.draw(Screen)
        self.WdwButton.draw(Screen)

        # オート速度
        self.NWButton.draw(Screen)
        self.FstButton.draw(Screen)
        self.NrlButton.draw(Screen)
        self.SlwButton.draw(Screen)

        if(self.gameFandamental.Data["tmp_Save"]["Scene_ID"] >= 0 ):
            self.SvButton.draw(Screen)
            self.LdButton.draw(Screen)
            self.TtlButton.draw(Screen)

        self.RtnButton.draw(Screen)

        self.MenuFullScreen.draw(Screen)
        self.MenuAutomaticRead.draw(Screen)
        self.MenuVoiceVolume.draw(Screen)
        self.MenuSoundVolume.draw(Screen)

        self.translucent_bou.draw(Screen)
        
        return
    
    def set_translucentPosition(self, pos):
        if(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Save"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Save"]["Pict"]["y"],self.gameFandamental.Data["Setting"]["Save"]["Pict"]["x"]+self.FSButton.get_rect(0) ,self.gameFandamental.Data["Setting"]["Save"]["Pict"]["y"]+ self.FSButton.get_rect(1))):
            # Save
            if(self.gameFandamental.Data["tmp_Save"]["Scene_ID"] >= 0 ): 
                self.translucent_bou.change_Coordinate((self.gameFandamental.Data["Setting"]["Save"]["x"],self.gameFandamental.Data["Setting"]["Save"]["y"]))
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Load"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Load"]["Pict"]["y"],self.gameFandamental.Data["Setting"]["Load"]["Pict"]["x"]+self.FSButton.get_rect(0) ,self.gameFandamental.Data["Setting"]["Load"]["Pict"]["y"]+ self.FSButton.get_rect(1))):
            # Load
            if(self.gameFandamental.Data["tmp_Save"]["Scene_ID"] >= 0 ): 
                self.translucent_bou.change_Coordinate((self.gameFandamental.Data["Setting"]["Load"]["x"],self.gameFandamental.Data["Setting"]["Load"]["y"]))
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Title"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Title"]["Pict"]["y"],self.gameFandamental.Data["Setting"]["Title"]["Pict"]["x"]+self.FSButton.get_rect(0) ,self.gameFandamental.Data["Setting"]["Title"]["Pict"]["y"]+ self.FSButton.get_rect(1))):
            # Title
            if(self.gameFandamental.Data["tmp_Save"]["Scene_ID"] >= 0 ): 
                self.translucent_bou.change_Coordinate((self.gameFandamental.Data["Setting"]["Title"]["x"],self.gameFandamental.Data["Setting"]["Title"]["y"]))
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Return"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Return"]["Pict"]["y"],self.gameFandamental.Data["Setting"]["Return"]["Pict"]["x"]+self.FSButton.get_rect(0) ,self.gameFandamental.Data["Setting"]["Return"]["Pict"]["y"]+ self.FSButton.get_rect(1))):
            # Return
            self.translucent_bou.change_Coordinate((self.gameFandamental.Data["Setting"]["Return"]["x"],self.gameFandamental.Data["Setting"]["Return"]["y"]))
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["noWait"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["noWait"]["Pict"]["y"],self.gameFandamental.Data["Setting"]["noWait"]["Pict"]["x"]+self.FSButton.get_rect(0) ,self.gameFandamental.Data["Setting"]["noWait"]["Pict"]["y"]+ self.FSButton.get_rect(1))):
            # 文字送り速度 ノーウェイト
            self.translucent_bou.change_Coordinate((self.gameFandamental.Data["Setting"]["noWait"]["x"],self.gameFandamental.Data["Setting"]["noWait"]["y"]))
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Fast"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Fast"]["Pict"]["y"],self.gameFandamental.Data["Setting"]["Fast"]["Pict"]["x"]+self.FSButton.get_rect(0) ,self.gameFandamental.Data["Setting"]["Fast"]["Pict"]["y"]+ self.FSButton.get_rect(1))):
            # 文字送り速度 ファスト
            self.translucent_bou.change_Coordinate((self.gameFandamental.Data["Setting"]["Fast"]["x"],self.gameFandamental.Data["Setting"]["Fast"]["y"]))
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Normal"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Normal"]["Pict"]["y"],self.gameFandamental.Data["Setting"]["Normal"]["Pict"]["x"]+self.FSButton.get_rect(0) ,self.gameFandamental.Data["Setting"]["Normal"]["Pict"]["y"]+ self.FSButton.get_rect(1))):
            # 文字送り速度 ノーマル
            self.translucent_bou.change_Coordinate((self.gameFandamental.Data["Setting"]["Normal"]["x"],self.gameFandamental.Data["Setting"]["Normal"]["y"]))
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Slow"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Slow"]["Pict"]["y"],self.gameFandamental.Data["Setting"]["Slow"]["Pict"]["x"]+self.FSButton.get_rect(0) ,self.gameFandamental.Data["Setting"]["Slow"]["Pict"]["y"]+ self.FSButton.get_rect(1))):
            # 文字送り速度 スロウ
            self.translucent_bou.change_Coordinate((self.gameFandamental.Data["Setting"]["Slow"]["x"],self.gameFandamental.Data["Setting"]["Slow"]["y"]))
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Full"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Full"]["Pict"]["y"],self.gameFandamental.Data["Setting"]["Full"]["Pict"]["x"]+self.FSButton.get_rect(0) ,self.gameFandamental.Data["Setting"]["Full"]["Pict"]["y"]+ self.FSButton.get_rect(1))):
            self.translucent_bou.change_Coordinate((self.gameFandamental.Data["Setting"]["Full"]["x"],self.gameFandamental.Data["Setting"]["Full"]["y"]))
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Window"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Window"]["Pict"]["y"],self.gameFandamental.Data["Setting"]["Window"]["Pict"]["x"] + self.WdwButton.get_rect(0),self.gameFandamental.Data["Setting"]["Window"]["Pict"]["y"]+self.WdwButton.get_rect(1))):
            self.translucent_bou.change_Coordinate((self.gameFandamental.Data["Setting"]["Window"]["x"],self.gameFandamental.Data["Setting"]["Window"]["y"]))
        else:
            self.translucent_bou.change_Coordinate((-100,-100))
        return


    def mouse_event(self, pos):
        if(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Save"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Save"]["Pict"]["y"],self.gameFandamental.Data["Setting"]["Save"]["Pict"]["x"]+self.FSButton.get_rect(0) ,self.gameFandamental.Data["Setting"]["Save"]["Pict"]["y"]+ self.FSButton.get_rect(1))):
            if(self.gameFandamental.Data["tmp_Save"]["Scene_ID"] >= 0 ): 
                return CurrentGameScene.NextGameOperation.GOTOSAVE
            return
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Load"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Load"]["Pict"]["y"],self.gameFandamental.Data["Setting"]["Load"]["Pict"]["x"]+self.FSButton.get_rect(0) ,self.gameFandamental.Data["Setting"]["Load"]["Pict"]["y"]+ self.FSButton.get_rect(1))):
            if(self.gameFandamental.Data["tmp_Save"]["Scene_ID"] >= 0 ): 
                return CurrentGameScene.NextGameOperation.GOTOLOAD
            return CurrentGameScene.NextGameOperation.NONE
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Title"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Title"]["Pict"]["y"],self.gameFandamental.Data["Setting"]["Title"]["Pict"]["x"]+self.FSButton.get_rect(0) ,self.gameFandamental.Data["Setting"]["Title"]["Pict"]["y"]+ self.FSButton.get_rect(1))):
            if(self.gameFandamental.Data["tmp_Save"]["Scene_ID"] >= 0 ): 
                if(MessageForeFront("確認","セーブしていない場合はデータは保存されません。タイトルに戻りますか。")):
                    return CurrentGameScene.NextGameOperation.GOTOTitle
            return CurrentGameScene.NextGameOperation.NONE
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Return"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Return"]["Pict"]["y"],self.gameFandamental.Data["Setting"]["Return"]["Pict"]["x"]+self.FSButton.get_rect(0) ,self.gameFandamental.Data["Setting"]["Return"]["Pict"]["y"]+ self.FSButton.get_rect(1))):
            return CurrentGameScene.NextGameOperation.RETURNTOPREVIEW
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["noWait"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["noWait"]["Pict"]["y"],self.gameFandamental.Data["Setting"]["noWait"]["Pict"]["x"]+self.FSButton.get_rect(0) ,self.gameFandamental.Data["Setting"]["noWait"]["Pict"]["y"]+ self.FSButton.get_rect(1))):
            # 文字送り速度 ノーウェイト
            self.gameFandamental.Config["Automatic_Character_Feed"] = "noWait"
            return CurrentGameScene.NextGameOperation.CHENGEAUTO
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Fast"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Fast"]["Pict"]["y"],self.gameFandamental.Data["Setting"]["Fast"]["Pict"]["x"]+self.FSButton.get_rect(0) ,self.gameFandamental.Data["Setting"]["Fast"]["Pict"]["y"]+ self.FSButton.get_rect(1))):
            # 文字送り速度 ファスト
            self.gameFandamental.Config["Automatic_Character_Feed"] = "Fast"
            return CurrentGameScene.NextGameOperation.CHENGEAUTO
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Normal"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Normal"]["Pict"]["y"],self.gameFandamental.Data["Setting"]["Normal"]["Pict"]["x"]+self.FSButton.get_rect(0) ,self.gameFandamental.Data["Setting"]["Normal"]["Pict"]["y"]+ self.FSButton.get_rect(1))):
            # 文字送り速度 ノーマル
            self.gameFandamental.Config["Automatic_Character_Feed"] = "Normal"
            return CurrentGameScene.NextGameOperation.CHENGEAUTO
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Slow"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Slow"]["Pict"]["y"],self.gameFandamental.Data["Setting"]["Slow"]["Pict"]["x"]+self.FSButton.get_rect(0) ,self.gameFandamental.Data["Setting"]["Slow"]["Pict"]["y"]+ self.FSButton.get_rect(1))):
            # 文字送り速度 スロウ
            self.gameFandamental.Config["Automatic_Character_Feed"] = "Slow"
            return CurrentGameScene.NextGameOperation.CHENGEAUTO
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Voice"]["Zero"]["x"],self.gameFandamental.Data["Setting"]["Voice"]["Zero"]["y"],self.gameFandamental.Data["Setting"]["Voice"]["Zero"]["x"]+self.MenuVoiceVolume.get_rect(0),self.gameFandamental.Data["Setting"]["Voice"]["Zero"]["y"]+self.MenuVoiceVolume.get_rect(1))):
            # ボイス音量を0にする
            self.gameFandamental.Config["VoiceVolume"] = "Zero"
            return CurrentGameScene.NextGameOperation.CHENGEVOICE
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Voice"]["Ten"]["x"],self.gameFandamental.Data["Setting"]["Voice"]["Ten"]["y"],self.gameFandamental.Data["Setting"]["Voice"]["Ten"]["x"]+self.MenuVoiceVolume.get_rect(0),self.gameFandamental.Data["Setting"]["Voice"]["Ten"]["y"]+self.MenuVoiceVolume.get_rect(1))):
            # ボイス音量を10にする
            self.gameFandamental.Config["VoiceVolume"] = "Ten"
            return CurrentGameScene.NextGameOperation.CHENGEVOICE
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Voice"]["Twenty"]["x"],self.gameFandamental.Data["Setting"]["Voice"]["Twenty"]["y"],self.gameFandamental.Data["Setting"]["Voice"]["Twenty"]["x"]+self.MenuVoiceVolume.get_rect(0),self.gameFandamental.Data["Setting"]["Voice"]["Twenty"]["y"]+self.MenuVoiceVolume.get_rect(1))):
            # ボイス音量を20にする
            self.gameFandamental.Config["VoiceVolume"] = "Twenty"
            return CurrentGameScene.NextGameOperation.CHENGEVOICE
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Voice"]["Thirty"]["x"],self.gameFandamental.Data["Setting"]["Voice"]["Thirty"]["y"],self.gameFandamental.Data["Setting"]["Voice"]["Thirty"]["x"]+self.MenuVoiceVolume.get_rect(0),self.gameFandamental.Data["Setting"]["Voice"]["Thirty"]["y"]+self.MenuVoiceVolume.get_rect(1))):
            # ボイス音量を30にする
            self.gameFandamental.Config["VoiceVolume"] = "Thirty"
            return CurrentGameScene.NextGameOperation.CHENGEVOICE
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Voice"]["Forty"]["x"],self.gameFandamental.Data["Setting"]["Voice"]["Forty"]["y"],self.gameFandamental.Data["Setting"]["Voice"]["Forty"]["x"]+self.MenuVoiceVolume.get_rect(0),self.gameFandamental.Data["Setting"]["Voice"]["Forty"]["y"]+self.MenuVoiceVolume.get_rect(1))):
            # ボイス音量を40にする
            self.gameFandamental.Config["VoiceVolume"] = "Forty"
            return CurrentGameScene.NextGameOperation.CHENGEVOICE
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Voice"]["Fifty"]["x"],self.gameFandamental.Data["Setting"]["Voice"]["Fifty"]["y"],self.gameFandamental.Data["Setting"]["Voice"]["Fifty"]["x"]+self.MenuVoiceVolume.get_rect(0),self.gameFandamental.Data["Setting"]["Voice"]["Fifty"]["y"]+self.MenuVoiceVolume.get_rect(1))):
            # ボイス音量を50にする
            self.gameFandamental.Config["VoiceVolume"] = "Fifty"
            return CurrentGameScene.NextGameOperation.CHENGEVOICE
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Voice"]["Sixty"]["x"],self.gameFandamental.Data["Setting"]["Voice"]["Sixty"]["y"],self.gameFandamental.Data["Setting"]["Voice"]["Sixty"]["x"]+self.MenuVoiceVolume.get_rect(0),self.gameFandamental.Data["Setting"]["Voice"]["Sixty"]["y"]+self.MenuVoiceVolume.get_rect(1))):
            # ボイス音量を60にする
            self.gameFandamental.Config["VoiceVolume"] = "Sixty"
            return CurrentGameScene.NextGameOperation.CHENGEVOICE
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Voice"]["Seventy"]["x"],self.gameFandamental.Data["Setting"]["Voice"]["Seventy"]["y"],self.gameFandamental.Data["Setting"]["Voice"]["Seventy"]["x"]+self.MenuVoiceVolume.get_rect(0),self.gameFandamental.Data["Setting"]["Voice"]["Seventy"]["y"]+self.MenuVoiceVolume.get_rect(1))):
            # ボイス音量を70にする
            self.gameFandamental.Config["VoiceVolume"] = "Seventy"
            return CurrentGameScene.NextGameOperation.CHENGEVOICE
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Voice"]["Eighty"]["x"],self.gameFandamental.Data["Setting"]["Voice"]["Eighty"]["y"],self.gameFandamental.Data["Setting"]["Voice"]["Eighty"]["x"]+self.MenuVoiceVolume.get_rect(0),self.gameFandamental.Data["Setting"]["Voice"]["Eighty"]["y"]+self.MenuVoiceVolume.get_rect(1))):
            # ボイス音量を80にする
            self.gameFandamental.Config["VoiceVolume"] = "Eighty"
            return CurrentGameScene.NextGameOperation.CHENGEVOICE
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Voice"]["Ninety"]["x"],self.gameFandamental.Data["Setting"]["Voice"]["Ninety"]["y"],self.gameFandamental.Data["Setting"]["Voice"]["Ninety"]["x"]+self.MenuVoiceVolume.get_rect(0),self.gameFandamental.Data["Setting"]["Voice"]["Ninety"]["y"]+self.MenuVoiceVolume.get_rect(1))):
            # ボイス音量を90にする
            self.gameFandamental.Config["VoiceVolume"] = "Ninety"
            return CurrentGameScene.NextGameOperation.CHENGEVOICE
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Voice"]["OneHundred"]["x"],self.gameFandamental.Data["Setting"]["Voice"]["OneHundred"]["y"],self.gameFandamental.Data["Setting"]["Voice"]["OneHundred"]["x"]+self.MenuVoiceVolume.get_rect(0),self.gameFandamental.Data["Setting"]["Voice"]["OneHundred"]["y"]+self.MenuVoiceVolume.get_rect(1))):
            # ボイス音量を100にする
            self.gameFandamental.Config["VoiceVolume"] = "OneHundred"
            return CurrentGameScene.NextGameOperation.CHENGEVOICE
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Sound"]["Zero"]["x"],self.gameFandamental.Data["Setting"]["Sound"]["Zero"]["y"],self.gameFandamental.Data["Setting"]["Sound"]["Zero"]["x"]+self.MenuVoiceVolume.get_rect(0),self.gameFandamental.Data["Setting"]["Sound"]["Zero"]["y"]+self.MenuVoiceVolume.get_rect(1))):
            # BGM音量を0にする
            self.gameFandamental.Config["SoundVolume"] = "Zero"
            return CurrentGameScene.NextGameOperation.CHENGESOUND
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Sound"]["Ten"]["x"],self.gameFandamental.Data["Setting"]["Sound"]["Ten"]["y"],self.gameFandamental.Data["Setting"]["Sound"]["Ten"]["x"]+self.MenuVoiceVolume.get_rect(0),self.gameFandamental.Data["Setting"]["Sound"]["Ten"]["y"]+self.MenuVoiceVolume.get_rect(1))):
            # BGM音量を10にする
            self.gameFandamental.Config["SoundVolume"] = "Ten"
            return CurrentGameScene.NextGameOperation.CHENGESOUND
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Sound"]["Twenty"]["x"],self.gameFandamental.Data["Setting"]["Sound"]["Twenty"]["y"],self.gameFandamental.Data["Setting"]["Sound"]["Twenty"]["x"]+self.MenuVoiceVolume.get_rect(0),self.gameFandamental.Data["Setting"]["Sound"]["Twenty"]["y"]+self.MenuVoiceVolume.get_rect(1))):
            # BGM音量を20にする
            self.gameFandamental.Config["SoundVolume"] = "Twenty"
            return CurrentGameScene.NextGameOperation.CHENGESOUND
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Sound"]["Thirty"]["x"],self.gameFandamental.Data["Setting"]["Sound"]["Thirty"]["y"],self.gameFandamental.Data["Setting"]["Sound"]["Thirty"]["x"]+self.MenuVoiceVolume.get_rect(0),self.gameFandamental.Data["Setting"]["Sound"]["Thirty"]["y"]+self.MenuVoiceVolume.get_rect(1))):
            # BGM音量を30にする
            self.gameFandamental.Config["SoundVolume"] = "Thirty"
            return CurrentGameScene.NextGameOperation.CHENGESOUND
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Sound"]["Forty"]["x"],self.gameFandamental.Data["Setting"]["Sound"]["Forty"]["y"],self.gameFandamental.Data["Setting"]["Sound"]["Forty"]["x"]+self.MenuVoiceVolume.get_rect(0),self.gameFandamental.Data["Setting"]["Sound"]["Forty"]["y"]+self.MenuVoiceVolume.get_rect(1))):
            # BGM音量を40にする
            self.gameFandamental.Config["SoundVolume"] = "Forty"
            return CurrentGameScene.NextGameOperation.CHENGESOUND
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Sound"]["Fifty"]["x"],self.gameFandamental.Data["Setting"]["Sound"]["Fifty"]["y"],self.gameFandamental.Data["Setting"]["Sound"]["Fifty"]["x"]+self.MenuVoiceVolume.get_rect(0),self.gameFandamental.Data["Setting"]["Sound"]["Fifty"]["y"]+self.MenuVoiceVolume.get_rect(1))):
            # BGM音量を50にする
            self.gameFandamental.Config["SoundVolume"] = "Fifty"
            return CurrentGameScene.NextGameOperation.CHENGESOUND
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Sound"]["Sixty"]["x"],self.gameFandamental.Data["Setting"]["Sound"]["Sixty"]["y"],self.gameFandamental.Data["Setting"]["Sound"]["Sixty"]["x"]+self.MenuVoiceVolume.get_rect(0),self.gameFandamental.Data["Setting"]["Sound"]["Sixty"]["y"]+self.MenuVoiceVolume.get_rect(1))):
            # BGM音量を60にする
            self.gameFandamental.Config["SoundVolume"] = "Sixty"
            return CurrentGameScene.NextGameOperation.CHENGESOUND
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Sound"]["Seventy"]["x"],self.gameFandamental.Data["Setting"]["Sound"]["Seventy"]["y"],self.gameFandamental.Data["Setting"]["Sound"]["Seventy"]["x"]+self.MenuVoiceVolume.get_rect(0),self.gameFandamental.Data["Setting"]["Sound"]["Seventy"]["y"]+self.MenuVoiceVolume.get_rect(1))):
            # BGM音量を70にする
            self.gameFandamental.Config["SoundVolume"] = "Seventy"
            return CurrentGameScene.NextGameOperation.CHENGESOUND
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Sound"]["Eighty"]["x"],self.gameFandamental.Data["Setting"]["Sound"]["Eighty"]["y"],self.gameFandamental.Data["Setting"]["Sound"]["Eighty"]["x"]+self.MenuVoiceVolume.get_rect(0),self.gameFandamental.Data["Setting"]["Sound"]["Eighty"]["y"]+self.MenuVoiceVolume.get_rect(1))):
            # BGM音量を80にする
            self.gameFandamental.Config["SoundVolume"] = "Eighty"
            return CurrentGameScene.NextGameOperation.CHENGESOUND
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Sound"]["Ninety"]["x"],self.gameFandamental.Data["Setting"]["Sound"]["Ninety"]["y"],self.gameFandamental.Data["Setting"]["Sound"]["Ninety"]["x"]+self.MenuVoiceVolume.get_rect(0),self.gameFandamental.Data["Setting"]["Sound"]["Ninety"]["y"]+self.MenuVoiceVolume.get_rect(1))):
            # BGM音量を90にする
            self.gameFandamental.Config["SoundVolume"] = "Ninety"
            return CurrentGameScene.NextGameOperation.CHENGESOUND
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Sound"]["OneHundred"]["x"],self.gameFandamental.Data["Setting"]["Sound"]["OneHundred"]["y"],self.gameFandamental.Data["Setting"]["Sound"]["OneHundred"]["x"]+self.MenuVoiceVolume.get_rect(0),self.gameFandamental.Data["Setting"]["Sound"]["OneHundred"]["y"]+self.MenuVoiceVolume.get_rect(1))):
            # BGM音量を100にする
            self.gameFandamental.Config["SoundVolume"] = "OneHundred"
            return CurrentGameScene.NextGameOperation.CHENGESOUND
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Full"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Full"]["Pict"]["y"],self.gameFandamental.Data["Setting"]["Full"]["Pict"]["x"]+self.FSButton.get_rect(0) ,self.gameFandamental.Data["Setting"]["Full"]["Pict"]["y"]+ self.FSButton.get_rect(1))):
            self.gameFandamental.Config["WindowMode"] = "Full"
            return CurrentGameScene.NextGameOperation.CHENGEDISPLAY
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["Setting"]["Window"]["Pict"]["x"],self.gameFandamental.Data["Setting"]["Window"]["Pict"]["y"],self.gameFandamental.Data["Setting"]["Window"]["Pict"]["x"] + self.WdwButton.get_rect(0),self.gameFandamental.Data["Setting"]["Window"]["Pict"]["y"]+self.WdwButton.get_rect(1))):
            self.gameFandamental.Config["WindowMode"] = "Window"
            return CurrentGameScene.NextGameOperation.CHENGEDISPLAY
        return CurrentGameScene.NextGameOperation.NONE

    def Saveing_Setting(self):

        # 暗号化したファイルを保存する
        with tempfile.TemporaryDirectory() as dname:
            # 一度、jsonファイルを一時ファイルに保存
            with open(os.path.join(dname, "Setting.json"), "w", encoding='utf-8') as file:
                json.dump(self.gameFandamental.Config, file, indent=2, ensure_ascii=False) 

            # 一時ファイルを開いて暗号化
            with open(os.path.join(dname, "Setting.json"), "rb") as file:
                setting = file.read()

            encrypted = file_encryped(setting)
            
            # 暗号化したファイルを保存
            with open('./Setting.xai', 'wb') as file:
                file.write(encrypted)
        
        #with open('./Setting.json', encoding="utf-8", mode="w") as jsonfile:
        #    json.dump(self.game_config, jsonfile, indent=2, ensure_ascii=False) 