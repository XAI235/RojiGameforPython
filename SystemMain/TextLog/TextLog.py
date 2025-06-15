import pygame
import textwrap
from SystemMain.SystemLib import *
from SystemMain.BaseClass import basescene

class TextLog(basescene):
    def __init__(self, gameFandamental : Game_Fandamental):
        # ゲーム素材など
        self.gameFandamental : Game_Fandamental = gameFandamental
        # ログデータ
        self.logs = []
        # 1行当たりの高さ
        self.line_height= 60
        # 現在のスクロール位置
        self.scroll_y = 0
        # オフセット
        self.y_offset = 0
        # 全体の高さ
        self.total_height = 0
        # (surface, y_position) のリスト
        self.visible_logs = []
        self.scrollbar_rect = None
        
        self.background : pygame.surface.Surface = pygame.image.load("./Data/save/tmp.png").convert_alpha()
        self.background.set_alpha(40)
        # マウスのボタン初期化
        self.pressedButton = (False, False, False)

    def initialize(self):
        text_data = self.gameFandamental.Text
        current_id = self.gameFandamental.Data["tmp_Save"]["Scene_ID"]

        # 1行の最大文字数
        wrap_width = 30

        for entry in text_data[:current_id+1]:
            if "message" in entry and "text" in entry["message"]:
                message = entry["message"]["text"]
                name = entry["message"].get("name")

                if (name is not None):
                    if "nazo" in name:
                        name = "???"
                    elif "tukasa" in name:
                        name = "司"
                    elif "tamaki" in name:
                        name = "環"
                    elif "sizuku" in name:
                        name = "雫"
                    elif "mio" in name:
                        name = "澪"    


                if name:
                    message = f"{name} : {message}"

                # /br を改行として扱う
                parts = message.split("/br")
                for part in parts:
                    wrapped_lined = textwrap.wrap(part, wrap_width)
                    self.logs.extend(wrapped_lined)

        # ログの順序が最後→最新が最初に変更
        self.total_height = len(self.logs) * self.line_height
        window_height = self.gameFandamental.Config["WindowHeight"]
        # 最新のログが画面の下端に表示されるように初期スクロール位置を設定
        self.scroll_y = min(0, window_height - self.total_height)
        return

    def update(self, Screen : pygame.surface.Surface, next_game_scene ,  changer, callback_Quit):
        ev = pygame.event.get()
        window_height = self.gameFandamental.Config["WindowHeight"]
        for event in ev:
            if (event.type == pygame.MOUSEWHEEL):
                self.scroll_y += event.y * 30 # 30 px スクロール
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                if event.button == 1 and self.scrollbar_rect and self.scrollbar_rect.collidepoint(event.pos):
                    self.dragging = True
                    self.drag_offset_y = event.pos[1] - self.scrollbar_rect.y
            elif (event.type == pygame.MOUSEBUTTONUP):
                if event.button == 1:
                    self.dragging = False
                elif event.button == 3:
                    self.gameFandamental.Data["tmp_Save"]["Scene_ID"] = -1
                    if(os.path.isfile("./Data/save/tmp.png")):
                        os.remove("./Data/save/tmp.png")
                    changer(CurrentGameScene.CurrentGameScene.RETURN)
                    return
            elif event.type == pygame.MOUSEMOTION:
                if getattr(self, 'dragging', False):
                    bar_height = self.get_scrollbar_height()
                    track_height = window_height
                    y = event.pos[1] - self.drag_offset_y
                    y = max(0, min(track_height - bar_height, y))
                    scroll_range = self.total_height - window_height
                    self.scroll_y = - (y / (track_height - bar_height)) * scroll_range
            elif (event.type == pygame.QUIT):
                if (MessageForeFront("確認", "終了いたしますか。")):
                    if(os.path.isfile("./Data/save/tmp.png")):
                        os.remove("./Data/save/tmp.png")
                    callback_Quit(False)
                    return
            self.pressedButton = pygame.mouse.get_pressed() # ここでマウスの状態を保存しているはず…。

        # スクロール範囲制限
        max_scroll = 0
        min_scroll = min(0, window_height - self.total_height)
        self.scroll_y = max(min_scroll, min(max_scroll, self.scroll_y))

        # 表示対象ログの準備
        self.visible_logs = []
        y_offset = self.scroll_y
        for log in self.logs:
            if -self.line_height < y_offset < window_height:
                text_surface = self.gameFandamental.Data["Font"]["Data"].render(log, True, (255, 255, 255))
                self.visible_logs.append((text_surface, y_offset))
            y_offset += self.line_height
            
        return
    
    def get_scrollbar_height(self):
        window_height = self.gameFandamental.Config["WindowHeight"]
        visible_ratio = window_height / max(1, self.total_height)
        return max(20, int(visible_ratio * window_height))

    def draw(self, Screen :pygame.surface.Surface):
        Screen.fill((30,30,30))

        Screen.blit(self.background, dest=(0,0), area= self.background.get_rect())

        for surface, y in self.visible_logs:
            Screen.blit(surface, (50, y))

        window_height = self.gameFandamental.Config["WindowHeight"]

        # スクロールバー描画
        if self.total_height > window_height:
            bar_width = 12
            bar_height = self.get_scrollbar_height()
            track_height = window_height
            scroll_range = self.total_height - track_height
            scroll_pos = -self.scroll_y / scroll_range * (track_height - bar_height)
            self.scrollbar_rect = pygame.Rect(self.gameFandamental.Config["WindowWidth"] - bar_width - 5, scroll_pos, bar_width, bar_height)
            pygame.draw.rect(Screen, (180, 180, 180), self.scrollbar_rect)
    
    
    def mouse_event(self):
        return super().mouse_event()
    
    def Changer_Scene(self):
        return super().Changer_Scene()
