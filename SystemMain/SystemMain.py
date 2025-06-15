import os
import sys
import json
import tempfile
import pygame
import datetime
from pygame.locals import *
from SystemMain.TitleScene import TitleScene
from SystemMain.GameScene import GameScene, CurrentGameScene
from SystemMain.Opening import Opening
from SystemMain.GameMenu import GameMenu
from SystemMain.LoadScene import LoadScene
from SystemMain.BaseClass import basescene
from SystemMain.SaveScene import SaveScene
from SystemMain.TextLog import TextLog
from SystemMain.SystemLib import *
from SystemMain.Ending import Ending
from SystemMain.Stack import stack
from SystemMain.Gallery import Gallery

ROOTPATH = os.path.dirname(os.path.abspath(__file__))
CFGPATH = os.path.dirname(ROOTPATH)

class SystemMain:
    def __init__(self):
        pygame.init()
        
        self.gameFandamental : Game_Fandamental = None
        self.game_config : dict = {}
        self.file_dir : dict = {}
        self.data : dict = {}
        self.text : dict = {}
        self.ending : dict = {}
        self.screen : pygame.surface.Surface
        self.clock = pygame.time.Clock()
        
        
    def __del__(self):
        return 
    
    def initialize(self):
        try:
            pygame.init()
            self.screen = pygame.display.set_mode((1,1), pygame.SCALED)  # 画面サイズ設定 # 小さな仮のウィンドウ
            pygame.mixer.init()
            pygame.font.init() 

            with tempfile.TemporaryDirectory() as dname:
                with open(os.path.join(os.getcwd(),'Data','image','Icon.xai'), 'rb') as file:
                    decryped = file_decryped(file.read())
                
                with open(os.path.join(dname, 'Icon.ico'), 'wb') as file:
                    file.write(decryped)
                pygame.display.set_icon(pygame.image.load(os.path.join(dname, 'Icon.ico'))) 
            pygame.display.set_caption("初期化中")                   # ウィンドウタイトル設定

            with tempfile.TemporaryDirectory() as dname:
                
                log = None
                if ("debugpy" in sys.modules):
                # ログ出力用
                    if(not(os.path.isdir(os.path.join("./", "Log")))):
                            #フォルダが存在しない場合はフォルダ作成
                            os.mkdir(os.path.join("./", "Log"))
                    log = open("./Log/Log" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".log", 'w')
                try:
                    
                    #self.gameFandamental = load_all_game_assets_from_encrypted_and_virtual("./", file_decryped)
                    if ("debugpy" in sys.modules):
                        log.write("復号を開始します\n")
                        # 設定ファイルの読み込み
                        log.write("./Setting.xaiの復号開始\n")
                    
                    with open('./Setting.xai', 'rb') as file:
                        # 暗号化されたファイルを読み込み復号
                        decrypted = file_decryped(file.read()) 
                        # 復号したファイルを一時ディレクトリに保存
                    with open(os.path.join(dname, "Setting.json"), "wb") as file:
                        file.write(decrypted)
                    with open(os.path.join(dname, "Setting.json"), "rb") as file:
                        self.game_config = json.load(file)
                    
                    if ("debugpy" in sys.modules):
                        log.write("./Setting.xaiの復号完了\n")
                        log.write("./File.xaiの復号開始\n")

                    # 素材画像ファイル名の読み込み
                    with open('./File.xai', 'rb') as file:
                        decryped = file_decryped(file.read())
                        with open(os.path.join(dname, "File.json"), "wb") as f:
                            f.write(decryped)
                        with open(os.path.join(dname, "File.json"), encoding='utf-8') as jsonfile:
                            self.file_dir = json.load(jsonfile)

                    if ("debugpy" in sys.modules):
                        log.write("./File.xaiの復号完了\n")

                    if self.game_config["WindowMode"] == "Window":
                        self.screen = pygame.display.set_mode((self.game_config["WindowWidth"],
                                            self.game_config["WindowHeight"]), pygame.SCALED)  # 画面サイズ設定
                    elif self.game_config["WindowMode"] == "Full":
                        self.screen = pygame.display.set_mode((self.game_config["WindowWidth"],
                                                            self.game_config["WindowHeight"]), pygame.FULLSCREEN | pygame.SCALED)  # 画面サイズ設定
                    
                    if ("debugpy" in sys.modules):
                        print(dname)

                    #os.mkdir(os.path.join(dname, "Data"))
                    CurrentDir = "./"
                    Datadir = os.path.join(CurrentDir, "Data")

                    #self.data = load_assets_from_json(self.file_dir, file_decryped, base_dir="./", max_workers=8)


                    #decrypt_and_write_all(Datadir, dname, file_decryped, log=log)

                    
                    # Dataの中身を探索
                    
                    for Current, dirs, files in os.walk(Datadir):
                        if("#" not in Current):
                            idx = Current.find(CurrentDir)
                            dir = Current[idx+len(CurrentDir):]
                            print(dir)
                            # フォルダの存在確認
                            if(not(os.path.isdir(os.path.join(dname, dir)))):
                                #フォルダが存在しない場合はフォルダ作成
                                os.mkdir(os.path.join(dname, dir))
                            # フォルダにファイルが存在しない場合はスキップする

                            if(len(files) != 0):
                                for i in range(len(files)):
                                    # 暗号化ファイル以外は全部無視
                                    if (".xai" in files[i]):
                                        fileName = files[i]

                                        if ("debugpy" in sys.modules):
                                            log.write(os.path.join("./", dir, fileName) + "の復号開始\n")

                                        with open(os.path.join(Current,fileName), "rb") as file:
                                            encrypted = file.read()

                                        # 復号
                                        decryped = file_decryped(encrypted)

                                        idx = fileName.find(".xai")
                                        # それぞれのファイル毎に拡張子決め
                                        if ("font" in Current):
                                            decrypedFileName = fileName[:idx] + ".ttf"
                                        elif ("image" in Current):
                                            if ("back" in Current):
                                                if("white" in fileName):
                                                    decrypedFileName = fileName[:idx] + ".png"
                                                else:
                                                    decrypedFileName = fileName[:idx] + ".jpg"
                                            elif("Icon" in fileName):
                                                decrypedFileName = fileName[:idx] + ".ico"
                                            else:
                                                decrypedFileName = fileName[:idx] + ".png"
                                        elif("save" in Current):
                                            if ("savedata" in fileName):
                                                decrypedFileName = fileName[:idx] + ".json"
                                            else:
                                                decrypedFileName = fileName[:idx] + ".png"
                                        elif("sound" in Current):
                                            decrypedFileName = fileName[:idx] + ".wav"
                                        elif("text"):
                                            decrypedFileName = fileName[:idx] + ".json"

                                        with open(os.path.join(dname, dir, decrypedFileName), 'wb') as file:
                                            file.write(decryped)
                                            del decryped
                                        
                                        if ("debugpy" in sys.modules):
                                            log.write(os.path.join("./", dir, fileName) + "の復号完了\n")
                        
                except :
                    if ("debugpy" in sys.modules):
                        log.close()
                    return False

                if ("debugpy" in sys.modules):
                    log.write("復号終了\n")
                    log.close()

                # 画像データを取り出し
                self.data = load_assets_from_json(self.file_dir, dname)

                with open(os.path.join(dname, "Data", "text", "Scenario_Data.json"), encoding='utf-8') as jsonfile:
                            self.text = json.load(jsonfile)

                self.text = load_assets_from_json(self.text, dname)

                with open(os.path.join(dname, "Data", "text", "Ending.json"), encoding='utf-8') as jsonfile:
                            self.ending = json.load(jsonfile)
    
        except FileNotFoundError:
            if ("debugpy" in sys.modules):
                print("ファイルが見つかりません")
            return False

        
        self.gameFandamental = Game_Fandamental(self.game_config, self.data, self.text, self.ending)

        # pygame.display.set_icon(pygame.image.load(self.file_dir["Icon"]["Data"]))
        #print("Icon:", self.gameFandamental.Data.get("Icon"))
        pygame.display.set_icon(self.gameFandamental.Data["Icon"]["Data"])

        pygame.display.set_caption(self.gameFandamental.Config["TitleName"])                   # ウィンドウタイトル設定
        
        if self.gameFandamental.Config["WindowMode"] == "Window":
            self.screen = pygame.display.set_mode((self.gameFandamental.Config["WindowWidth"],
                                self.gameFandamental.Config["WindowHeight"]), pygame.SCALED)  # 画面サイズ設定
        elif self.gameFandamental.Config["WindowMode"] == "Full":
            self.screen = pygame.display.set_mode((self.gameFandamental.Config["WindowWidth"],
                                self.gameFandamental.Config["WindowHeight"]), pygame.FULLSCREEN | pygame.SCALED)  # 画面サイズ設定


        self.NowGameState : CurrentGameScene.GameState = CurrentGameScene.GameState.NORMAL

        # 親クラスのシーンの変数をインスタンス
        self.game_state : basescene = None
        self.game_stack : stack.MyStack = stack.MyStack()

        # 子クラスを親クラスのインスタンスに代入。
        # これにより、子クラスを入れ替えることが可能。
        #self.game_state = TitleScene.TitleScene(self.game_config, self.file_dir, self.screen)
        self.game_state = Opening.OpeningScene(self.gameFandamental, self.screen)
        
        self.game_state.initialize()
        return True

    def main_loop(self):
        self.running = True
        self.current_game_scene = CurrentGameScene.CurrentGameScene.TITLE_SCENE
        self.next_game_scene = CurrentGameScene.CurrentGameScene.NONE_SCENE
        while(self.running):
            self.clock.tick(30) # 30fpsに設定
            if self.NowGameState == CurrentGameScene.GameState.NORMAL:
                self.game_state.update(self.screen, self.current_game_scene, self.Changer_Scene, self.finalize)
            
            self.game_state.draw(self.screen)

            pygame.display.flip()                             # 画面更新 必ず必要

        pygame.quit()

    def finalize(self, Finish : bool = True):
        
        self.running = Finish

    
    def Changer_Scene(self, next_scene : CurrentGameScene.CurrentGameScene = CurrentGameScene.CurrentGameScene.NONE_SCENE,now_scene: CurrentGameScene.CurrentGameScene = CurrentGameScene.CurrentGameScene.NONE_SCENE):
        
        if(next_scene ==CurrentGameScene.CurrentGameScene.TITLE_SCENE): # タイトルシーンの処理
            self.game_state = TitleScene.TitleScene(self.gameFandamental, self.screen)
            self.game_state.initialize()
            self.game_stack.all_remove()
        elif(next_scene ==CurrentGameScene.CurrentGameScene.INTRO): # タイトルシーンの処理
            while( self.game_stack.len() > 1 ):
                self.game_stack.pop()
            self.game_stack.push(self.game_state)
            self.game_state = GameScene.GameScene(self.gameFandamental, self.screen)
            self.game_state.initialize()
        elif(next_scene == CurrentGameScene.CurrentGameScene.LOAD) :
            self.game_stack.push(self.game_state)
            self.game_state = LoadScene.LoadScene(self.gameFandamental)
            self.game_state.initialize()
        elif(next_scene == CurrentGameScene.CurrentGameScene.SAVE) :
            self.game_stack.push(self.game_state)
            self.game_state = SaveScene.SaveScene(self.gameFandamental)
            self.game_state.initialize()
        elif(next_scene == CurrentGameScene.CurrentGameScene.TEXTLOG) :
            self.game_stack.push(self.game_state)
            self.game_state = TextLog.TextLog(self.gameFandamental)
            self.game_state.initialize()
            return
        elif(next_scene == CurrentGameScene.CurrentGameScene.SETTING) :
            self.game_stack.push(self.game_state)
            self.game_state = GameMenu.GameMenu(self.gameFandamental)
            self.game_state.initialize()
        elif(next_scene == CurrentGameScene.CurrentGameScene.RETURN) :
            self.game_state = self.game_stack.pop()
        elif(next_scene == CurrentGameScene.CurrentGameScene.ENDING):
            self.game_stack.push(self.game_state)
            self.game_state = Ending.Ending(self.gameFandamental, self.screen)
            self.game_state.initialize()
        elif(next_scene == CurrentGameScene.CurrentGameScene.GALLERY):
            self.game_stack.push(self.game_state)
            self.game_state = Gallery.GalleryScene(self.gameFandamental, self.screen)
            self.game_state.initialize()
        elif(next_scene == CurrentGameScene.CurrentGameScene.QUIT) :
            self.running = not(MessageForeFront("確認", "セーブしていない場合はデータは保存されません。終了いたしますか。"))
            if(os.path.isfile("./Data/save/tmp.png")):
                os.remove("./Data/save/tmp.png")