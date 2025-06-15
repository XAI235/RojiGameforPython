import os
import pygame
import queue
from pygame.locals import *
from SystemMain.MouseClass import MouseClass
from SystemMain.BaseClass import basescene
from SystemMain.GameScene import GameScene,CurrentGameScene
from SystemMain.LoadScene import LoadScene
from SystemMain.SystemLib import *

class Ending(basescene) :
    #def __init__(self, game_config : dict , file_dir : dict, screen : pygame.surface.Surface):
    def __init__(self, gameFandamental : Game_Fandamental, screen : pygame.surface.Surface):
        #self.game_config : dict = game_config
        #self.file_dir : dict = file_dir
        self.gameFandamental = gameFandamental
        self.Ending = self.gameFandamental.End
        self.pictures = self.Ending_Picures(self.gameFandamental)
        self.BGM : GameSound = GameSound(gameFandamental)
        self.EndingId :int = None
        self.Counter : int = None
        self.time :list = []
        self.Background : BackgroundPicture = BackgroundPicture()
        self.Timer : Timer = Timer

    def initialize(self):
        self.Background.Regist_order_Picture("Background", 
                                             pygame.transform.scale(self.gameFandamental.Data["Story"]["Picture"]["black"], 
                                                                    (self.gameFandamental.Config["WindowWidth"],self.gameFandamental.Config["WindowHeight"])), 
                                             (0,0))
        
        #with open('./Data/text/Ending.json', encoding='utf-8') as jsonfile:
        #    self.Ending = json.load(jsonfile)

        self.EndingId = 0
        self.Counter = 1

        self.pictures.initialize(self.Ending, self.gameFandamental.Config)


        self.BGM.start_BGM(self.gameFandamental.Data["Ending"]["BGM"])  

    def update(self, Screen : pygame.surface.Surface, next_game_scene ,  changer, callback_Quit):
        
        for event in pygame.event.get():

            button = pygame.mouse.get_pressed()
            if event.type == QUIT:                          # 終了ボタンを押した場合終了 セーブ警告あり
                if (MessageForeFront("確認", "終了いたしますか。")):
                    if(os.path.isfile("./Data/save/tmp.png")):
                        os.remove("./Data/save/tmp.png")
                    callback_Quit(False)

        if(self.pictures.update(changer)):
            self.gameFandamental.Config["Cleared"] = 1
            self.BGM.fadeout_BGM(4000)
            with tempfile.TemporaryDirectory() as dname:
                with open(os.path.join(dname, 'Setting.json'), encoding="utf-8", mode="w") as jsonfile:
                    json.dump(self.gameFandamental.Config, jsonfile, indent=2, ensure_ascii=False)
                
                # 一時ファイルを開いて暗号化
                with open(os.path.join(dname, "Setting.json"), "rb") as file:
                    setting = file.read()

                encrypted = file_encryped(setting)
                
                # 暗号化したファイルを保存
                with open('./Setting.xai', 'wb') as file:
                    file.write(encrypted)
                    
        return 

    def draw(self, Screen :pygame.surface.Surface):
        self.Background.draw(Screen)
        self.pictures.draw(Screen)

    class Ending_Picures:
        def __init__(self, gameFandamental : Game_Fandamental):
            self.gameFandamental : Game_Fandamental = gameFandamental
            self.Data : list = []
            self.Rect : list = []
            self.Coordinate : list[tuple] = []
            self.time : list = []
            #self.font_kinds :pygame.font.Font = gameFandamental.Data["Font"]["Data"]
            self.BufferData : list = []
            self.BufferRect : list = []
            self.BufferCoor : list[tuple] = []
            self.Timer : Timer = Timer()
            self.x:int = 0
            self.y:int = 0
            self.thanks : MonoPicture = MonoPicture()
            self.finish : bool = False
            self.Next : bool = False
            #self.config : dict = gameFandamental.Config

        def initialize(self, ending_data : list, game_config : dict):
            self.config = game_config
            for i in range(len(ending_data)):
                data = ending_data[i]
                if "Pict" in data:
                    pict = self.gameFandamental.Data["Title_Scene"][data["Pict"]]["Data"]
                    self.Data.append(pict)
                    self.Rect.append(pict.get_rect())
                    self.Coordinate.append(((game_config["WindowWidth"] - pict.get_rect()[2])/2, game_config["WindowHeight"]))
                elif "Text" in data:
                    pict = self.Get_TextPicture(data["Text"])
                    self.Data.append(pict)
                    self.Rect.append(pict.get_rect())
                    self.Coordinate.append(((game_config["WindowWidth"] - pict.get_rect()[2])/2, game_config["WindowHeight"]))
        
                if "StartTime" in data:
                    self.time.append(data["StartTime"])
                    

            pict = self.Get_TextPicture("Thanks you for playing!!")
            self.x = (game_config["WindowWidth"] - pict.get_rect()[2])/2
            self.y = game_config["WindowHeight"]
            self.thanks.Regist_order_Picture("Thanks", pict, (self.x,self.y))
            


            self.Timer.set_timer(self.time.pop(0))
            self.Timer.timer_start()

        def Get_TextPicture(self, text : str) -> pygame.surface.Surface :
            return self.gameFandamental.Data["Font"]["Data"].render(text, True, (255,255,255)).convert_alpha()

        def update(self, changer):
            if (not(self.finish)):
                if(self.Timer.check_time()):
                    self.BufferData.append(self.Data.pop(0))
                    self.BufferRect.append(self.Rect.pop(0))
                    self.BufferCoor.append(self.Coordinate.pop(0))
                    if len(self.time) != 0 :
                        self.Timer.set_timer(self.time.pop(0))
                        self.Timer.timer_start()
                    else:
                        self.Timer.stop_Timer()
            
                if(len(self.BufferData) != 0):
                    coor = self.BufferCoor[0]
                    rect = self.BufferRect[0]
                    if(rect[3]== (-1) * coor[1]):
                        self.BufferData.pop(0)
                        self.BufferRect.pop(0)
                        self.BufferCoor.pop(0)
                    for i in range(len(self.BufferCoor)):
                        x = self.BufferCoor[i][0]
                        y = self.BufferCoor[i][1] - 1
                        self.BufferCoor[i] = (x,y)

                if((len(self.BufferData) == 0) and len(self.time) == 0):
                    self.finish = True
            else:
                if(self.y > (self.config["WindowHeight"] - self.thanks.get_rect(1))/2):
                    self.y -= 1
                    self.thanks.change_Coordinate((self.x,self.y))
                else:
                    if(not(self.Next)):
                        self.Timer.set_timer(8)
                        self.Timer.timer_start()
                        self.Next = True
                        return True
                    else:
                        if(self.Timer.check_time()):
                            self.Timer.stop_Timer()
                            self.thanks.change_FadeMode("OUT")
                                    
                        if(self.thanks.check_Alpha(0)):
                            changer(CurrentGameScene.CurrentGameScene.TITLE_SCENE)
                    
            self.Timer.update()
            return False

        def draw(self, Screen :pygame.surface.Surface):

            if(not(self.finish)):
                for i in range(len(self.BufferData)):
                    Screen.blit(self.BufferData[i], dest=self.BufferCoor[i], area=self.BufferRect[i])
            else:
                self.thanks.draw(Screen)
