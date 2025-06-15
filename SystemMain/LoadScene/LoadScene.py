import os
import json
import pygame
import tempfile
from tkinter import messagebox
from pygame.locals import *
from SystemMain.GameScene import CurrentGameScene
from SystemMain.MouseClass import MouseClass
from SystemMain.BaseClass import basescene
from SystemMain.SystemLib import *

class LoadScene(basescene) :

    _PREVIEW : int = -1
    _NEXT : int = 1
    _MAX_DISPLAY_SAVE_DATA :int = 4

#    def __init__(self, game_config : dict , file_dir : dict) :
    def __init__(self, gameFandamental : Game_Fandamental) :
        ############################################ 変数初期化 #############################################################
        #self.game_config : dict = game_config
        #self.file_dir : dict = file_dir
        self.gameFandamental : Game_Fandamental = gameFandamental

        self.Background : BackgroundPicture = BackgroundPicture()
        self.save_data_constellation = {}

        # ################################## #
        # ボタン用変数                        #
        # 0 : Next Button                    #
        # 1 : Preview Button                 #
        # 2 : Home Button                    #
        # ################################## #
        self.Button : Multiple_Picture = Multiple_Picture()
        self.pressedButton = (False,False,False) # ボタン押し状態
        self.story_len : list[int] = []
        self.date : list[str] = []
        self.Save_data_Name : list[pygame.surface.Surface] = []
        self.image : dict = {}
        self.nextState : CurrentGameScene.LoadState = None
        self.story_len_buffer : list[pygame.surface.Surface] = []
        self.date_buffer : list[pygame.surface.Surface] = []
        self.page_Num : pygame.surface.Surface = None
        #self.font_kinds = pygame.font.Font("./Data/font/ShipporiMincho-Regular.ttf", 32)
        self.save_img : Multiple_Picture = Multiple_Picture()
        ######################################################################################################################    
    
    def initialize(self) :
        self.Background.Regist_order_Picture("Load", 
                                             pygame.transform.scale(self.gameFandamental.Data["SavingAndLoading"]["BackGround"]["Data"],
                                                                    (self.gameFandamental.Config["WindowWidth"],self.gameFandamental.Config["WindowHeight"])), 
                                                                    (0,0))

        self.Button.Regist_Pictures("Next", 
                                    self.gameFandamental.Data["SavingAndLoading"]["Next"]["Data"], 
                                    (self.gameFandamental.Data["SavingAndLoading"]["Next"]["x"],self.gameFandamental.Data["SavingAndLoading"]["Next"]["y"]))
        self.Button.Regist_Pictures("Preview", 
                                    self.gameFandamental.Data["SavingAndLoading"]["Preview"]["Data"],
                                    (self.gameFandamental.Data["SavingAndLoading"]["Preview"]["x"],self.gameFandamental.Data["SavingAndLoading"]["Preview"]["y"]))
        self.Button.Regist_Pictures("Return", 
                                    self.gameFandamental.Data["SavingAndLoading"]["Return"]["Data"],
                                    (self.gameFandamental.Data["SavingAndLoading"]["Return"]["x"],self.gameFandamental.Data["SavingAndLoading"]["Return"]["y"]))

        with tempfile.TemporaryDirectory() as dname:
            print(dname)
            for item in os.listdir('./Data/save/'):
                if("#" not in item):
                    if("savedata.xai" in item):
                        with open(os.path.join('./Data/save/', item), "rb") as file:
                            decryped = file_decryped(file.read())
                        # ここの間に文字切り出しを入れる
                        idx = item.find(".xai")
                        with open(os.path.join(dname, item[:idx] + ".json"), 'wb') as file:
                            file.write(decryped)

                        with open(os.path.join(dname, item[:idx] + ".json"), 'rb') as file:
                            self.save_data_constellation = json.load(file)
                    elif (("save_data" in item) and (".xai" in item)):
                        with open(os.path.join('./Data/save/', item), "rb") as file:
                            decryped = file_decryped(file.read())
                        # ここの間に文字切り出しを入れる
                        idx = item.find(".xai")
                        with open(os.path.join(dname, item[:idx] + ".png"), 'wb') as file:
                            file.write(decryped)
                        
                        self.image[item[:idx]]= pygame.image.load(os.path.join(dname, item[:idx] + ".png"))

                    print(list)
            
            with open(os.path.join('./Data/Font/ShipporiMincho-Regular.xai', ), "rb") as file:
                decryped = file_decryped(file.read())

            # 同じデータから複数サイズのフォントオブジェクトを作成可能
            font_bytes_io = io.BytesIO(decryped)
            self.font = pygame.font.Font(font_bytes_io, 24)

        self.save_position = 0
        self.data_position = 0

        self.image["black"] = self.gameFandamental.Data["Story"]["Picture"]["black"]

        #self.page_Num = self.font_kinds.render(str(self.save_position+1) + "/4", True, (0,0,0))
        self.page_Num = self.gameFandamental.Data["Font"]["Data"].render(str(self.save_position+1) + "/4", True, (0,0,0))

        for i in range(LoadScene._MAX_DISPLAY_SAVE_DATA):
            self.story_len.append(self.save_data_constellation["save_data" + str(4*self.save_position + i + 1)]["Scene_ID"])
            self.date.append(self.save_data_constellation["save_data" + str(4*self.save_position + i + 1)]["Save_Date"])  

        for i in range(LoadScene._MAX_DISPLAY_SAVE_DATA):
            self.Save_data_Name.append(self.font.render("Save Data" + str(4*self.save_position + i + 1), True, (0,0,0)))
            if self.date[i] == "yyyy-mm-dd" :
                self.date_buffer.append(self.font.render("No Data", True, (0,0,0)))
            else:
                self.date_buffer.append(self.font.render(self.date[i], True, (0,0,0)))
        
        for i in range(self.save_data_constellation["Fandamental_data"]["MAX_SAVE_DATA"]):
            self.save_img.Regist_order_Pictures("save_data"+str(i+1), 
                                                pygame.transform.scale(self.image[self.save_data_constellation["save_data"+str(i + 1)]["image"]],
                                                                        (self.save_data_constellation["Fandamental_data"]["IMG"]["x"],
                                                                        self.save_data_constellation["Fandamental_data"]["IMG"]["y"])),
                                                                            (self.save_data_constellation["Fandamental_data"]["IMG_POS_S"]["x"] + (i%2) * self.save_data_constellation["Fandamental_data"]["IMG_DEF"]["x"],
                                                                            self.save_data_constellation["Fandamental_data"]["IMG_POS_S"]["y"] + ((i//2)%2) * self.save_data_constellation["Fandamental_data"]["IMG_DEF"]["y"]))
            
            if(self.save_data_constellation["save_data"+str(i + 1)]["image"] == "black"):
                self.save_img.set_alpha(0, i)

        
    def update(self, Screen : pygame.surface.Surface, next_game_scene ,  changer, callback_Quit) :
        ############################################### セーブ内容の表示 #####################################################
        self.Save_data_Name.clear()
        self.date_buffer.clear()

        for i in range(LoadScene._MAX_DISPLAY_SAVE_DATA):
            self.Save_data_Name.append(self.font.render("Save Data" + str(4*self.save_position + i + 1), True, (0,0,0)))
            if self.date[i] == "yyyy-mm-dd" :
                self.date_buffer.append(self.font.render("No Data", True, (0,0,0)))
            else:
                self.date_buffer.append(self.font.render(self.date[i], True, (0,0,0)))

        self.page_Num = self.gameFandamental.Data["Font"]["Data"].render(str(self.save_position+1) + "/4", True, (0,0,0))
        #####################################################################################################################

        ############################################### マウスの挙動 #####################################################
        for event in pygame.event.get():
            
            if ((event.type == pygame.MOUSEBUTTONUP) and self.pressedButton[0]):
                self.nextState = self.mouse_event(pygame.mouse.get_pos)
                if(self.nextState == CurrentGameScene.LoadState.RETRUN):
                    changer(CurrentGameScene.CurrentGameScene.RETURN)
                    return
                elif(self.nextState == CurrentGameScene.LoadState.PREVIEWTOSAVEDATA):
                    self.load_anothor_savedata(LoadScene._PREVIEW)
                    return
                elif(self.nextState == CurrentGameScene.LoadState.NEXTTOSAVEDATA):
                    self.load_anothor_savedata(LoadScene._NEXT)
                    return
                elif(self.nextState == CurrentGameScene.LoadState.LOAD):
                    if(self.Loading_SaveData()):
                        pygame.mixer.music.stop()
                        changer(CurrentGameScene.CurrentGameScene.INTRO)
                else:
                    return
            elif event.type == QUIT:                          # 終了ボタンを押した場合終了 セーブ警告あり
                if (MessageForeFront("確認", "終了いたしますか。")):
                    if(os.path.isfile("./Data/save/tmp.png")):
                        os.remove("./Data/save/tmp.png")
                    callback_Quit(False)
                #callback_Quit(not(messagebox.askyesno("確認", "終了いたしますか。")))
            self.pressedButton = pygame.mouse.get_pressed()
        #####################################################################################################################
        
        return 0
    
    def draw(self, Screen:pygame.surface.Surface) : 
        ############################### 背景とボタンの描画 ###################################################
        self.Background.draw(Screen)
        self.Button.draw(Screen)

        Screen.blit(self.page_Num, dest=(630,660), area=self.page_Num.get_rect())
        #####################################################################################################
        
        self.save_img.draw_mult(Screen, 4*self.save_position)

        ####################################### 文字の描画 ###################################################
        for i in range(LoadScene._MAX_DISPLAY_SAVE_DATA//2):
            for j in range(LoadScene._MAX_DISPLAY_SAVE_DATA//2):
                Screen.blit(self.Save_data_Name[i*2+j], dest=(240+j*540, 322+i*320), area=self.Save_data_Name[i*2+j].get_rect())
                Screen.blit(self.date_buffer[i*2+j], dest=(390+j*540, 322+i*320), area=self.date_buffer[i*2+j].get_rect())
        #####################################################################################################
        return 0   

    def mouse_event(self, pos):
        if(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["SavingAndLoading"]["Return"]["x"],
                                                        self.gameFandamental.Data["SavingAndLoading"]["Return"]["y"],
                                                        self.gameFandamental.Data["SavingAndLoading"]["Return"]["x"] + self.Button.get_Dict_Rect("Return", 0),
                                                        self.gameFandamental.Data["SavingAndLoading"]["Return"]["y"] + self.Button.get_Dict_Rect("Return", 1))):
            # Title画面に戻る
            return CurrentGameScene.LoadState.RETRUN
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["SavingAndLoading"]["Preview"]["x"],
                                                        self.gameFandamental.Data["SavingAndLoading"]["Preview"]["y"],
                                                        self.gameFandamental.Data["SavingAndLoading"]["Preview"]["x"] + self.Button.get_Dict_Rect("Preview", 0),
                                                        self.gameFandamental.Data["SavingAndLoading"]["Preview"]["y"] + self.Button.get_Dict_Rect("Preview", 1))):
            # 前へ
            return CurrentGameScene.LoadState.PREVIEWTOSAVEDATA
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,self.gameFandamental.Data["SavingAndLoading"]["Next"]["x"],
                                                        self.gameFandamental.Data["SavingAndLoading"]["Next"]["y"],
                                                        self.gameFandamental.Data["SavingAndLoading"]["Next"]["x"] + self.Button.get_Dict_Rect("Next", 0),
                                                        self.gameFandamental.Data["SavingAndLoading"]["Next"]["y"] + self.Button.get_Dict_Rect("Next", 1))):
            # 次へ
            return CurrentGameScene.LoadState.NEXTTOSAVEDATA
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                          self.save_data_constellation["Fandamental_data"]["IMG_POS_S"]["x"],
                                                          self.save_data_constellation["Fandamental_data"]["IMG_POS_S"]["y"],
                                                          self.save_data_constellation["Fandamental_data"]["IMG_POS_S"]["x"]+self.save_data_constellation["Fandamental_data"]["IMG"]["x"],
                                                          self.save_data_constellation["Fandamental_data"]["IMG_POS_S"]["y"]+self.save_data_constellation["Fandamental_data"]["IMG"]["y"])):
            self.data_position = 1
            return CurrentGameScene.LoadState.LOAD
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                          self.save_data_constellation["Fandamental_data"]["IMG_POS_S"]["x"]+self.save_data_constellation["Fandamental_data"]["IMG_DEF"]["x"],
                                                          self.save_data_constellation["Fandamental_data"]["IMG_POS_S"]["y"],
                                                          self.save_data_constellation["Fandamental_data"]["IMG_POS_S"]["x"]+self.save_data_constellation["Fandamental_data"]["IMG_DEF"]["x"]+self.save_data_constellation["Fandamental_data"]["IMG"]["x"],
                                                          self.save_data_constellation["Fandamental_data"]["IMG_POS_S"]["y"]+self.save_data_constellation["Fandamental_data"]["IMG"]["y"])):
            self.data_position = 2
            return CurrentGameScene.LoadState.LOAD
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                          self.save_data_constellation["Fandamental_data"]["IMG_POS_S"]["x"],
                                                          self.save_data_constellation["Fandamental_data"]["IMG_POS_S"]["y"]+self.save_data_constellation["Fandamental_data"]["IMG_DEF"]["y"],
                                                          self.save_data_constellation["Fandamental_data"]["IMG_POS_S"]["x"]+self.save_data_constellation["Fandamental_data"]["IMG"]["x"],
                                                          self.save_data_constellation["Fandamental_data"]["IMG_POS_S"]["y"]+self.save_data_constellation["Fandamental_data"]["IMG_DEF"]["y"]+self.save_data_constellation["Fandamental_data"]["IMG"]["y"])):
            self.data_position = 3
            return CurrentGameScene.LoadState.LOAD
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,
                                                          self.save_data_constellation["Fandamental_data"]["IMG_POS_S"]["x"]+self.save_data_constellation["Fandamental_data"]["IMG_DEF"]["x"],
                                                          self.save_data_constellation["Fandamental_data"]["IMG_POS_S"]["y"]+self.save_data_constellation["Fandamental_data"]["IMG_DEF"]["y"],
                                                          self.save_data_constellation["Fandamental_data"]["IMG_POS_S"]["x"]+self.save_data_constellation["Fandamental_data"]["IMG_DEF"]["x"]+self.save_data_constellation["Fandamental_data"]["IMG"]["x"],
                                                          self.save_data_constellation["Fandamental_data"]["IMG_POS_S"]["y"]+self.save_data_constellation["Fandamental_data"]["IMG_DEF"]["y"]+self.save_data_constellation["Fandamental_data"]["IMG"]["y"])):
            self.data_position = 4
            return CurrentGameScene.LoadState.LOAD
        else:
            return CurrentGameScene.CurrentGameScene.NONE_SCENE

    
    def load_anothor_savedata(self, IncrementAndDecrease : int) :
        self.story_len.clear()
        self.date.clear()

        self.save_position += IncrementAndDecrease

        if (self.save_position >= 4) : 
            self.save_position = 3
        elif(self.save_position <= -1):
            self.save_position = 0

        ############################################ セーブデータ更新 #########################################################
        for i in range(LoadScene._MAX_DISPLAY_SAVE_DATA):
            self.story_len.append(self.save_data_constellation["save_data" + str(4*self.save_position + i + 1)]["Scene_ID"])
            self.date.append(self.save_data_constellation["save_data" + str(4*self.save_position + i + 1)]["Save_Date"])  
       ######################################################################################################################

        return
    
    def Loading_SaveData(self):
        if self.save_data_constellation["save_data"+ str(4*self.save_position + self.data_position)]["Save_Date"]  != "yyyy-mm-dd" :
            if MessageForeFront("確認", "セーブデータ"+ str(4*self.save_position + self.data_position) + "をロードしますか。") :
                self.gameFandamental.Data["tmp_Save"]["Scene_ID"] = self.save_data_constellation["save_data"+ str(4*self.save_position + self.data_position)]["Scene_ID"]
                self.gameFandamental.Data["tmp_Save"]["BackGround"]["Data"] = self.save_data_constellation["save_data"+ str(4*self.save_position + self.data_position)]["BackGround"]["Data"]
                #self.gameFandamental.Data["tmp_Save"]["BackGround"]["Name"] = self.save_data_constellation["save_data"+ str(4*self.save_position + self.data_position)]["BackGround"]["Name"]
                self.gameFandamental.Data["tmp_Save"]["BGM"] = self.save_data_constellation["save_data"+ str(4*self.save_position + self.data_position)]["BGM"] 
                # messagebox.showinfo('セーブ完了', "セーブデータ"+ str(4*self.save_position + self.data_position) + "を呼び出しました。")
                return True
        else :
            MessageForefrontShowwarning("警告", "セーブデータ"+ str(4*self.save_position + self.data_position) + "にはセーブデータが保存されていません。")
            return False