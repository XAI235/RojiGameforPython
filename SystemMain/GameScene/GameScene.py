import os
import pygame
import json
from pygame.locals import *
from SystemMain.MouseClass import MouseClass
from SystemMain.GameScene import CurrentGameScene
from SystemMain.BaseClass import basescene
from SystemMain.SystemLib import * 

class GameScene(basescene) :

    MAX_COL = 35 # 1行の最大文字数
    MAX_ROW = 3 # 1回の表示で表示できる最大行数

    #def __init__(self, game_config : dict , file_dir : dict, screen : pygame.surface.Surface) :
    def __init__(self, gameFandamental : Game_Fandamental, screen : pygame.surface.Surface) :

        # ここら辺の変数をまとめたい(希望)
        #self.game_config : dict = game_config
        #self.file_dir : dict = file_dir

        self.gameFandamental : Game_Fandamental = gameFandamental

        self.MainPictureDict : BasePicture = BasePicture() # データクラス格納用変数 メインクラスの保存をする
        self.current_line : int = 0 # 読み込んだテキストデータの行数
        self.textlog : list = [] # 今まで読んだセリフのログ
        self.logline : int = 0 # ログの行数
        self.pressedButton = (False,False,False) # ボタン押し状態
        self.GameSoundData : GameSound = GameSound(gameFandamental)
        self.NowSceneStatus : CurrentGameScene = CurrentGameScene.CurrentGameStatus.WAITTING
        self.CanRead : bool = True
        
        if(self.GameSoundData.busy()):
            self.GameSoundData.stop_BGM()

        # 暫定セーブデータを初期化
        if self.gameFandamental.Data["tmp_Save"]["Scene_ID"] < 0:
            self.gameFandamental.Data["tmp_Save"]["Scene_ID"] = 0
        
        #クラス固有の変数にするとシナリオ読み切ったときに再度初めからにできない
        #インスタンス変数にして対応
        self.scenario = []
        self.scene_id = self.gameFandamental.Data["tmp_Save"]["Scene_ID"]
        self.draw_functions = []
        self.Timer : Timer = Timer()

        self.Screen : Screen_Manager = Screen_Manager(self.gameFandamental, screen)

        if self.gameFandamental.Data["tmp_Save"]["Scene_ID"] > 0:
            self.Screen.set_Background(self.gameFandamental.Data["tmp_Save"]["BackGround"]["Data"])
        
        if self.gameFandamental.Data["tmp_Save"]["BGM"] != "" :
            self.GameSoundData.start_BGM(self.gameFandamental.Data["tmp_Save"]["BGM"])


        # フォントのインスタンスを初期化
        if not(pygame.font.get_init()):
            pygame.font.init()

        return
    
    def __del__(self):
        return
    
    def initialize(self) :
        #with open('./File.dat','r', encoding='utf-8') as f:
        #    line : str = f.readline()
        #    while line:
        #        words = line[:-1].split(',')
        #        self.MainPictureDict.Picutre_Append(words[0],words[1])
        #        line = f.readline()
        
        #with open('./Data/text/Scenario_Data.json', encoding='utf-8') as f:
        #    self.scenario = json.load(f)
        self.scenario = self.gameFandamental.Text

        if self.scene_id == 0:
            self.scene_id += 1
        
        self.current_scene = self.scenario[self.scene_id]
        self.Screen.Register_ScreenInfo(self.MainPictureDict, self.current_scene)
        self.Timer.set_timer(self.gameFandamental.Data["Setting"][self.gameFandamental.Config["Automatic_Character_Feed"]]["value"]) # 任意の時間にセット　(デバッグ用に99999秒に設定中)
        return 0
    
    def update(self, Screen : pygame.surface.Surface, next_game_scene ,  changer, callback_Quit):
        ev = pygame.event.get()
        pos = pygame.mouse.get_pos
        for event in ev:
            if(((event.type == pygame.MOUSEBUTTONUP) and self.pressedButton[0]) and self.CanRead):
                gamescene = self.mouse_event(pos)
                if gamescene == CurrentGameScene.CurrentGameScene.NONE_SCENE:
                    self.GameSoundData.voice_Stop()
                    self.scene_id += 1
                    if self.scene_id >= len(self.scenario):
                        pygame.quit()
                    else:
                        self.current_scene = self.scenario[self.scene_id]
                        self.Screen.Register_ScreenInfo(self.MainPictureDict, self.current_scene)
                        self.Timer.reset()
                elif gamescene == CurrentGameScene.CurrentGameScene.SAVE:
                    self.gameFandamental.Data["tmp_Save"]["Scene_ID"] = self.scene_id
                    self.Timer.stop_Timer()
                    self.Screen.save_image()
                    changer(gamescene)
                elif gamescene == CurrentGameScene.CurrentGameScene.LOAD:
                    self.Timer.stop_Timer()
                    changer(gamescene)
                elif gamescene == CurrentGameScene.CurrentGameScene.TEXTLOG:
                    self.gameFandamental.Data["tmp_Save"]["Scene_ID"] = self.scene_id
                    self.Timer.stop_Timer()
                    self.Screen.save_image()
                    changer(gamescene)
                elif gamescene == CurrentGameScene.CurrentGameScene.SETTING:
                    self.gameFandamental.Data["tmp_Save"]["Scene_ID"] = self.scene_id
                    self.Timer.stop_Timer
                    self.Screen.save_image()
                    changer(gamescene)
                elif gamescene == CurrentGameScene.CurrentGameScene.AUTO:
                    self.Timer.set_timer(self.gameFandamental.Data["Setting"][self.gameFandamental.Config["Automatic_Character_Feed"]]["value"]) # 任意の時間にセット　(デバッグ用に99999秒に設定中)
                    self.Timer.Turn_Timer()
                    self.Screen.change_SystemButton("Auto")
            elif (event.type == pygame.MOUSEBUTTONUP) and self.pressedButton[2]:
                self.Screen.undisplay_textwindow()
                self.CanRead = self.CanRead ^ True
                if(not(self.Timer.check_pouse())):
                    self.Timer.pouse_Timer()
                else:
                    self.Timer.restart_Timer()
                """self.file_dir["tmp_Save"]["Scene_ID"] = self.scene_id
                self.Timer.stop_Timer
                self.Screen.save_image()
                changer(CurrentGameScene.CurrentGameScene.SETTING)"""
            elif event.type == QUIT:    
                if (MessageForeFront("確認", "終了いたしますか。")):
                    if(os.path.isfile("./Data/save/tmp.png")):
                        os.remove("./Data/save/tmp.png")
                    callback_Quit(False)
                #callback_Quit(not(messagebox.askyesno("確認", "終了いたしますか。")))
            self.pressedButton = pygame.mouse.get_pressed() # ここでマウスの状態を保存しているはず…。

        # 必ず最後のテキストでタイマーを止める。
        if (len(self.scenario) - 3 == self.scene_id and self.Timer.check_start()):
            self.Timer.stop_Timer()

        if (len(self.scenario) - 2 == self.scene_id and not(self.Timer.check_start())):
            self.Timer.set_timer(5)
            self.Timer.Turn_Timer()

        if(self.Timer.check_time()):
            self.GameSoundData.voice_Stop()
            self.scene_id += 1
            if self.scene_id >= len(self.scenario):
                pygame.quit()
            else:
                self.current_scene = self.scenario[self.scene_id]
                self.Screen.Register_ScreenInfo(self.MainPictureDict, self.current_scene)

        if(not(self.Timer.check_finish_time(self.gameFandamental.Data["Setting"][self.gameFandamental.Config["Automatic_Character_Feed"]]["value"])) and len(self.scenario) - 2 != self.scene_id):
            self.Timer.set_timer(self.gameFandamental.Data["Setting"][self.gameFandamental.Config["Automatic_Character_Feed"]]["value"])

        if 'END' in self.current_scene.keys():
            self.Timer.stop_Timer()
            self.GameSoundData.stop_BGM()
            changer(CurrentGameScene.CurrentGameScene.ENDING)

        if(self.mouse_event(pos) == CurrentGameScene.CurrentGameScene.SAVE):
            self.Screen.change_SystemButton("Save",1)
        elif(self.mouse_event(pos) == CurrentGameScene.CurrentGameScene.LOAD):
            self.Screen.change_SystemButton("Load",1)
        elif(self.mouse_event(pos) == CurrentGameScene.CurrentGameScene.TEXTLOG):
            self.Screen.change_SystemButton("TextLog",1)
        elif(self.mouse_event(pos) == CurrentGameScene.CurrentGameScene.SETTING):
            self.Screen.change_SystemButton("Setting",1)
        else:
            self.Screen.change_SystemButton("Clear")


        self.Timer.update()
            

    def draw(self, Screen :pygame.surface.Surface) :
        self.Screen.draw()


    
    def mouse_event(self, pos):
        if(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Story"]["Picture"]["autobuttonplay"]["x"],
                                                        self.gameFandamental.Data["Story"]["Picture"]["autobuttonplay"]["y"],
                                                        self.gameFandamental.Data["Story"]["Picture"]["autobuttonplay"]["x"]+self.gameFandamental.Data["Story"]["Picture"]["autobuttonplay"]["0"].get_rect()[2],
                                                        self.gameFandamental.Data["Story"]["Picture"]["autobuttonplay"]["y"]+self.gameFandamental.Data["Story"]["Picture"]["autobuttonplay"]["0"].get_rect()[3])):
            # オートボタン
            return CurrentGameScene.CurrentGameScene.AUTO
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Story"]["Picture"]["savebutton"]["x"],
                                                        self.gameFandamental.Data["Story"]["Picture"]["savebutton"]["y"],
                                                        self.gameFandamental.Data["Story"]["Picture"]["savebutton"]["x"]+self.gameFandamental.Data["Story"]["Picture"]["savebutton"]["0"].get_rect()[2],
                                                        self.gameFandamental.Data["Story"]["Picture"]["savebutton"]["y"]+self.gameFandamental.Data["Story"]["Picture"]["savebutton"]["0"].get_rect()[3])):
            # セーブボタン
            return CurrentGameScene.CurrentGameScene.SAVE
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Story"]["Picture"]["loadbutton"]["x"],
                                                        self.gameFandamental.Data["Story"]["Picture"]["loadbutton"]["y"],
                                                        self.gameFandamental.Data["Story"]["Picture"]["loadbutton"]["x"]+self.gameFandamental.Data["Story"]["Picture"]["loadbutton"]["0"].get_rect()[2],
                                                        self.gameFandamental.Data["Story"]["Picture"]["loadbutton"]["y"]+self.gameFandamental.Data["Story"]["Picture"]["loadbutton"]["0"].get_rect()[3])):
            # ロードボタン
            return CurrentGameScene.CurrentGameScene.LOAD
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Story"]["Picture"]["Logbutton"]["x"],
                                                        self.gameFandamental.Data["Story"]["Picture"]["Logbutton"]["y"],
                                                        self.gameFandamental.Data["Story"]["Picture"]["Logbutton"]["x"]+self.gameFandamental.Data["Story"]["Picture"]["Logbutton"]["0"].get_rect()[2],
                                                        self.gameFandamental.Data["Story"]["Picture"]["Logbutton"]["y"]+self.gameFandamental.Data["Story"]["Picture"]["Logbutton"]["0"].get_rect()[3])):
            # ロードボタン
            return CurrentGameScene.CurrentGameScene.TEXTLOG
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                        self.gameFandamental.Data["Story"]["Picture"]["Setting"]["x"],
                                                        self.gameFandamental.Data["Story"]["Picture"]["Setting"]["y"],
                                                        self.gameFandamental.Data["Story"]["Picture"]["Setting"]["x"]+self.gameFandamental.Data["Story"]["Picture"]["Setting"]["0"].get_rect()[2],
                                                        self.gameFandamental.Data["Story"]["Picture"]["Setting"]["y"]+self.gameFandamental.Data["Story"]["Picture"]["Setting"]["0"].get_rect()[3])):
            # セッティングボタン
            return CurrentGameScene.CurrentGameScene.SETTING
        else:
            # それ以外は話を進める
            return CurrentGameScene.CurrentGameScene.NONE_SCENE
            