import pygame
import os
import json
import sys
import io
import tempfile
from cryptography.fernet import Fernet
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
#import GameManager
from pygame.locals import *
from SystemMain.MouseClass import MouseClass
from SystemMain.GameScene import CurrentGameScene
from SystemMain.BaseClass import basescene
from tkinter import Tk,messagebox
from dataclasses import dataclass


# 設定とファイルを扱う構造体
@dataclass
class Game_Fandamental:
    Config : dict
    Data: dict
    Text : dict
    End : dict

# 分岐対象の拡張子リスト
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ICON_EXTENSIONS = {".ico"}
SOUND_EXTENSIONS = {".wav"}
FONT_EXTENSIONS = {".ttf"}

#画像を分割してクラスにするのではなく
#一つにまとめるのありだったりするか…？

"""
def load_assets_from_json(json_data, temp_root):
    def walk_and_load(node):
        if isinstance(node, dict):
            if "Data" in node and isinstance(node["Data"], str) and os.path.splitext(node["Data"])[1]:
                file_path = os.path.join(temp_root, node["Data"])
                asset = load_file_by_extension(file_path)
                result = dict(node)
                result["Data"] = asset  # Data に読み込んだファイルを上書き
                return result
            else:
                return {k: walk_and_load(v) for k, v in node.items()}
        elif isinstance(node, str) and os.path.splitext(node)[1]:
            file_path = os.path.join(temp_root, node)
            return load_file_by_extension(file_path)
        else:
            return node

    return walk_and_load(json_data)
"""
def load_assets_from_json(json_data, temp_root, max_workers=8):
    cache = {}
    cache_lock = Lock()

    def load_and_cache(path):
        abs_path = os.path.join(temp_root, path)
        with cache_lock:
            if path in cache:
                return cache[path]
        asset = load_file_by_extension(abs_path)
        with cache_lock:
            cache[path] = asset
        return asset

    def walk_and_load(node):
        if isinstance(node, dict):
            if "Data" in node and isinstance(node["Data"], str) and os.path.splitext(node["Data"])[1]:
                asset = executor.submit(load_and_cache, node["Data"]).result()
                result = dict(node)
                result["Data"] = asset
                return result
            else:
                return {k: walk_and_load(v) for k, v in node.items()}
        elif isinstance(node, str) and os.path.splitext(node)[1]:
            return executor.submit(load_and_cache, node).result()
        else:
            return node

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return walk_and_load(json_data)



def load_file_by_extension(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    try:
        if ext in IMAGE_EXTENSIONS:
            image = pygame.image.load(file_path)
            if ext == ".png":
                return image.convert_alpha()
            else:
                return image.convert()
        elif ext in ICON_EXTENSIONS:
            return pygame.image.load(file_path)
        elif ext in SOUND_EXTENSIONS:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            return pygame.mixer.Sound(file_path)
        elif ext in FONT_EXTENSIONS:
            if not pygame.font.get_init():
                pygame.font.init()
            with open(file_path, 'rb') as f:
                font_data = f.read()
            font_io = io.BytesIO(font_data)
            return pygame.font.Font(font_io, 32)
        else:
            return f"[未対応の拡張子: {ext}]"
    except Exception as e:
        return f"[読み込み失敗: {e}]"

def decrypt_and_write_all(datadir, dname, file_decryped, log=None, max_workers=8):
    def gather_files():
        #復号対象となる .xai ファイルを一覧化
        tasks = []
        for current, dirs, files in os.walk(datadir):
            if "#" not in current:
                rel_dir = os.path.relpath(current, start="./")
                os.makedirs(os.path.join(dname, rel_dir), exist_ok=True)
                for fname in files:
                    if fname.endswith(".xai"):
                        full_path = os.path.join(current, fname)
                        tasks.append((full_path, rel_dir, fname))
        return tasks

    def get_decrypted_name(current_dir, filename):
        idx = filename.find(".xai")
        name = filename[:idx]
        # 拡張子判断ロジック
        if "font" in current_dir:
            return name + ".ttf"
        elif "image" in current_dir:
            if "back" in current_dir:
                return name + ".png" if "white" in filename else name + ".jpg"
            elif "Icon" in filename:
                return name + ".ico"
            else:
                return name + ".png"
        elif "save" in current_dir:
            return name + ".json" if "savedata" in filename else name + ".png"
        elif "sound" in current_dir:
            return name + ".wav"
        elif "text" in current_dir:
            return name + ".json"
        return name + ".json"

    def decrypt_file_task(full_path, rel_dir, fname):
        try:
            if log:
                log.write(f"{os.path.join('./', rel_dir, fname)} の復号開始\n")

            with open(full_path, "rb") as f:
                encrypted = f.read()
            decrypted = file_decryped(encrypted)
            decrypted_name = get_decrypted_name(rel_dir, fname)
            out_path = os.path.join(dname, rel_dir, decrypted_name)
            with open(out_path, "wb") as out:
                out.write(decrypted)

            if log:
                log.write(f"{os.path.join('./', rel_dir, fname)} の復号完了\n")
        except Exception as e:
            if log:
                log.write(f"{full_path} の復号失敗: {e}\n")

    # 並列実行開始
    tasks = gather_files()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(decrypt_file_task, full_path, rel_dir, fname)
            for full_path, rel_dir, fname in tasks
        ]
        for _ in as_completed(futures):
            pass  # 完了待ち
#------------------------------------------------------------------------------------------------------------------------------------
def load_assets_from_json_memory(json_data, file_decryped, base_dir="./Data", max_workers=8):
    cache = {}
    lock = Lock()

    def load_and_cache(rel_path):
        with lock:
            if rel_path in cache:
                return cache[rel_path]

        abs_path = os.path.join(base_dir, rel_path)
        with open(abs_path, "rb") as f:
            encrypted = f.read()
        decrypted = file_decryped(encrypted)
        asset = load_from_bytes(rel_path, decrypted)

        with lock:
            cache[rel_path] = asset
        return asset

    def walk_and_load(node):
        if isinstance(node, dict):
            if "Data" in node and isinstance(node["Data"], str) and os.path.splitext(node["Data"])[1]:
                asset = executor.submit(load_and_cache, node["Data"]).result()
                result = dict(node)
                result["Data"] = asset
                return result
            else:
                return {k: walk_and_load(v) for k, v in node.items()}
        elif isinstance(node, str) and os.path.splitext(node)[1]:
            return executor.submit(load_and_cache, node).result()
        else:
            return node

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return walk_and_load(json_data)
#----------------------------------------------------------------------------------------------------
"""
def load_all_game_assets_from_encrypted_and_virtual(base_dir, file_decryped, max_workers=8):
    # ファイルパス構築
    setting_enc_path = os.path.join(base_dir, "Setting.xai")
    file_enc_path = os.path.join(base_dir, "File.xai")
    scenario_enc_path = os.path.join(base_dir, "Data", "text", "Scenario_Data.xai")
    ending_enc_path = os.path.join(base_dir, "Data", "text", "Ending.xai")

    # ① JSONの復号・読み込み
    with open(setting_enc_path, "rb") as f:
        config = json.loads(file_decryped(f.read()).decode('utf-8'))

    with open(file_enc_path, "rb") as f:
        file_dir = json.loads(file_decryped(f.read()).decode('utf-8'))

    with open(scenario_enc_path, "rb") as f:
        text = json.loads(file_decryped(f.read()).decode('utf-8'))

    with open(ending_enc_path, "rb") as f:
        ending = json.loads(file_decryped(f.read()).decode('utf-8'))

    # ② Data/以下の仮想ファイル（素材ファイル）復号・読み込み
    data = {}

    def decrypt_and_load(full_path):
        try:
            with open(full_path, "rb") as f:
                encrypted = f.read()
            decrypted = file_decryped(encrypted)

            # 正しい拡張子で仮想ファイル名を構成
            corrected_filename = guess_decrypted_filename(full_path)

            # ロード処理
            return load_from_bytes(corrected_filename, decrypted)
        except Exception as e:
            return f"[素材読み込み失敗: {e}]"

    # スレッドプールで高速並列探索
    futures = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for current, dirs, files in os.walk(os.path.join(base_dir, "Data")):
            for file in files:
                if file.endswith(".xai"):
                    full_path = os.path.join(current, file)
                    relative_path = os.path.relpath(full_path, base_dir)
                    relative_path = relative_path.replace("\\", "/")
                    futures[relative_path] = executor.submit(decrypt_and_load, full_path)

    # 読み込み結果を整理
    loaded_data = {path.replace(".xai", ""): future.result() for path, future in futures.items()}

    # ③ file_dir 構造に読み込んだ素材をマージする
    def walk_and_replace(node):
        if isinstance(node, dict):
            if "Data" in node:
                data_path = node["Data"]
                if data_path in loaded_data:
                    node["Data"] = loaded_data[data_path]
                else:
                    node["Data"] = f"[データ無し: {data_path}]"
            for k, v in node.items():
                node[k] = walk_and_replace(v)
        return node

    data = walk_and_replace(file_dir)

    return Game_Fandamental(
        config=config,
        text=text,
        ending=ending,
        data=data
    )
# -----------------------------------------------------------------------------------------------------
def guess_decrypted_filename(full_path):
    base = full_path.replace("\\", "/")
    name = os.path.basename(base)
    dir_part = os.path.dirname(base).lower()

    idx = name.find(".xai")
    name = name[:idx]

    if "font" in dir_part:
        return name + ".ttf"
    elif "image" in dir_part:
        if "back" in dir_part:
            return name + ".png" if "white" in name else name + ".jpg"
        elif "icon" in name.lower():
            return name + ".ico"
        else:
            return name + ".png"
    elif "sound" in dir_part:
        return name + ".wav"
    elif "save" in dir_part:
        return name + ".json" if "savedata" in name else name + ".png"
    elif "text" in dir_part:
        return name + ".json"
    else:
        return name + ".dat"

#------------------------------------------------------------------------------------
"""
def load_from_bytes(filename, data_bytes):
    ext = os.path.splitext(filename)[1].lower()
    try:
        buffer = io.BytesIO(data_bytes)
        if ext in IMAGE_EXTENSIONS:
            image = pygame.image.load(buffer)
            return image.convert_alpha() if ext == ".png" else image.convert()
        elif ext in ICON_EXTENSIONS:
            return pygame.image.load(buffer)
        elif ext in SOUND_EXTENSIONS:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            return pygame.mixer.Sound(buffer)
        elif ext in FONT_EXTENSIONS:
            return pygame.font.Font(buffer, 32)
        else:
            return f"[未対応の拡張子: {ext}]"
    except Exception as e:
        return f"[読み込み失敗: {e}]"

"""
# -----------------------------------------------------------------------------------
# === ファイル拡張子推定 ===
def guess_decrypted_filename(current_dir, file_name):
    dir_lower = current_dir.lower()
    name = os.path.splitext(file_name)[0]

    if "font" in dir_lower:
        return name + ".ttf"
    elif "image" in dir_lower:
        if "back" in dir_lower:
            return name + ".png" if "white" in name else name + ".jpg"
        elif "icon" in name.lower():
            return name + ".ico"
        else:
            return name + ".png"
    elif "sound" in dir_lower:
        return name + ".wav"
    elif "save" in dir_lower:
        return name + ".json" if "savedata" in name else name + ".png"
    elif "text" in dir_lower:
        return name + ".json"
    else:
        return name + ".dat"
    
# === 統合読み込み処理（並列復号版） ===
def load_all_game_assets_from_encrypted_and_virtual(base_dir, file_decryped, max_workers=8):
    temp_dir = tempfile.mkdtemp()

    if not pygame.mixer.get_init():
        pygame.mixer.init()

    # 暗号化JSONを復号・保存・読み込み
    def decrypt_json(xai_path, save_as):
        with open(xai_path, "rb") as f:
            decrypted = file_decryped(f.read())
        save_path = os.path.join(temp_dir, save_as)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(decrypted)
        with open(save_path, encoding="utf-8") as f:
            return json.load(f)

    config = decrypt_json(os.path.join(base_dir, "Setting.xai"), "Setting.json")
    file_dir = decrypt_json(os.path.join(base_dir, "File.xai"), "File.json")
    text = decrypt_json(os.path.join(base_dir, "Data", "text", "Scenario_Data.xai"), os.path.join("Data", "text", "Scenario_Data.json"))
    ending = decrypt_json(os.path.join(base_dir, "Data", "text", "Ending.xai"), os.path.join("Data", "text", "Ending.json"))

    # Data配下の素材ファイル復号＆保存（並列化）
    tasks = []
    for current, dirs, files in os.walk(os.path.join(base_dir, "Data")):
        if "#" in os.path.basename(current):
            continue
        rel_dir = os.path.relpath(current, base_dir)
        for file_name in files:
            if file_name.endswith(".xai"):
                full_path = os.path.join(current, file_name)
                save_name = guess_decrypted_filename(current, file_name)
                save_path = os.path.join(temp_dir, rel_dir, save_name)
                tasks.append((full_path, save_path))

    def decrypt_and_save(full_path, save_path):
        with open(full_path, "rb") as f:
            encrypted = f.read()
        decrypted = file_decryped(encrypted)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(decrypted)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(decrypt_and_save, full, save) for full, save in tasks]
        for future in futures:
            future.result()

    # file_dirに基づいてファイルをpygameで読み込み
    def load_asset(rel_path):
        abs_path = os.path.join(temp_dir, rel_path)
        ext = os.path.splitext(abs_path)[1].lower()

        try:
            if ext in IMAGE_EXTENSIONS:
                image = pygame.image.load(abs_path)
                return image.convert_alpha() if ext == ".png" else image.convert()
            elif ext in ICON_EXTENSIONS:
                return pygame.image.load(abs_path)
            elif ext in SOUND_EXTENSIONS:
                return pygame.mixer.Sound(abs_path)
            elif ext in FONT_EXTENSIONS:
                if not pygame.font.get_init():
                    pygame.font.init()
                return pygame.font.Font(abs_path, 32)
            else:
                return f"[未対応の拡張子: {ext}]"
        except Exception as e:
            return f"[読み込み失敗: {e}]"
    def load_asset(rel_path):
        abs_path = os.path.join(temp_dir, rel_path)
        ext = os.path.splitext(abs_path)[1].lower()

        try:
            if ext in IMAGE_EXTENSIONS:
                image = pygame.image.load(abs_path)
                return image.convert_alpha() if ext == ".png" else image.convert()
            elif ext in ICON_EXTENSIONS:
                return pygame.image.load(abs_path)
            elif ext in SOUND_EXTENSIONS:
                if not pygame.mixer.get_init():
                    pygame.mixer.init()
                return pygame.mixer.Sound(abs_path)
            elif ext in FONT_EXTENSIONS:
                if not pygame.font.get_init():
                    pygame.font.init()
                return pygame.font.Font(abs_path, 32)
            else:
                return f"[未対応の拡張子: {ext}]"
        except Exception as e:
            return f"[読み込み失敗: {e}]"
    def walk_and_load(node):
        if isinstance(node, dict):
            if "Data" in node and isinstance(node["Data"], str):
                asset = load_asset(node["Data"])
                result = dict(node)
                result["Data"] = asset
                return result
            else:
                return {k: walk_and_load(v) for k, v in node.items()}
        else:
            return node

    data = walk_and_load(file_dir)
    def walk_and_load_parallel(node):
        results = {}
        tasks = []
        def schedule(node, parent, key):
            if isinstance(node, dict):
                if "Data" in node and isinstance(node["Data"], str):
                    tasks.append((parent, key, node["Data"]))
                else:
                    for k, v in node.items():
                        schedule(v, node, k)

        schedule(node, None, None)
        def schedule(node, parent, key):
            if isinstance(node, dict):
                for k, v in node.items():
                    schedule(v, node, k)
            elif isinstance(node, str):
                ext = os.path.splitext(node)[1].lower()
                if ext in IMAGE_EXTENSIONS | ICON_EXTENSIONS | SOUND_EXTENSIONS | FONT_EXTENSIONS:
                    tasks.append((parent, key, node))
        def schedule(n, parent, key):
            if isinstance(n, dict):
                if "Data" in n and isinstance(n["Data"], str):
                    tasks.append((n, "Data", n["Data"]))
                else:
                    for k, v in n.items():
                        schedule(v, n, k)
            elif isinstance(n, str):
                ext = os.path.splitext(n)[1].lower()
                if ext in IMAGE_EXTENSIONS | ICON_EXTENSIONS | SOUND_EXTENSIONS | FONT_EXTENSIONS:
                    tasks.append((parent, key, n))
        def schedule(n, parent, key):
            if isinstance(n, dict):
                if "Data" in n and isinstance(n["Data"], str):
                    tasks.append((n, "Data", n["Data"]))
                else:
                    for k, v in n.items():
                        schedule(v, n, k)
            elif isinstance(n, str):
                ext = os.path.splitext(n)[1].lower()
                if ext in IMAGE_EXTENSIONS | ICON_EXTENSIONS | SOUND_EXTENSIONS | FONT_EXTENSIONS:
                    tasks.append((parent, key, n))
                    
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_key = {executor.submit(load_asset, path): (parent, key) for parent, key, path in tasks}
            for future in future_to_key:
                parent, key = future_to_key[future]
                result = future.result()
                if parent is None:
                    continue
                parent[key]["Data"] = result

        return node

    data = walk_and_load_parallel(file_dir)

    return Game_Fandamental(
        Config=config,
        Data=data,
        Text=text,
        End=ending
    )
"""




# 最初に画像を登録しておくクラス。
# 読み込まれた画像は辞書型で格納
class BasePicture:
    # 初期化
    def __init__(self) : 
        self.Data : dict = {}

    # 画像の登録。辞書に追加しておく、この時、画像の名前を一緒に登録しておくことで、
    # 呼び出しを容易にしておく
    def Picutre_Append(self, baceDir : str, PictureName : list[str], Picture_Data : list[str]) :
        self.Data[PictureName] = pygame.image.load(Picture_Data).convert_alpha()

    # 画像のデータを返す関数
    def get_Picture_Data(self, PictureName : list[str]) : 
        return self.Data[PictureName]
    
    def dict_search(d, ext):
        key = d.keys()
    
# 画像を表示させるためのバッファークラス
# 表示画像の登録や再配置、削除、描画などの関数がある。
# 一度登録されているかどうかも確認できるようにすれば、いいのかな？
class BackgroundPicture:
    # 初期化
    def __init__(self):
        #self.Pictuer_Order : list = []
        self.Data = None
        self.Rect = None
        self.Coordinate = None
        self.Alpha = 0
        self.Fade = "Normal"

    # 表示画像登録関数
    def Regist_order_Picture(self, Picture_Name: list[str], Picture_Data : pygame.surface.Surface,  Coordinate : tuple, FadeCode : str = "Normal") :
        self.Data = Picture_Data
        self.Rect = Picture_Data.get_rect()
        self.Coordinate = Coordinate
        self.Data.set_alpha(255)
        self.FadeCode = FadeCode

    def change_Picture_Size(self, size: tuple):
        self.Data = pygame.transform.scale(self.Data,size)
        self.Rect = self.Data.get_rect()

    # 画像の描画
    def draw(self, Screen :pygame.surface.Surface):
        Screen.fill((0, 0, 0))

        if(self.Data != None):
            if(self.FadeCode != "Normal"):
                Alpha = 0 if self.FadeCode=="IN" else 255
                Alpha = Fader.Fade(Screen, self.FadeCode, self.Data,self.Coordinate, Alpha)
                self.Data.set_alpha(Alpha)
                self.FadeCode = "Normal"
    
            Screen.blit(self.Data, dest=self.Coordinate, area=self.Rect)

            # 画像を表示させるためのバッファークラス
# 表示画像の登録や再配置、削除、描画などの関数がある。
# 一度登録されているかどうかも確認できるようにすれば、いいのかな？
class MonoPicture:
    # 初期化
    def __init__(self):
        #self.Pictuer_Order : list = []
        self.Data = None
        self.Rect = None
        self.Coordinate = None
        self.Alpha =255
        self.Fade = "Normal"

    # 表示画像登録関数
    def Regist_order_Picture(self, Picture_Name: list[str], Picture_Data : pygame.surface.Surface,  Coordinate : tuple, FadeCode : str = "Normal") :
        self.Data = Picture_Data
        self.Rect = Picture_Data.get_rect()
        self.Coordinate = Coordinate
        self.FadeCode = FadeCode

    def change_Picture_Size(self, size: tuple):
        self.Data = pygame.transform.scale(self.Data,size)
        self.Rect = self.Data.get_rect()

    def change_Coordinate(self, coor : tuple):
        self.Coordinate = coor

    def change_FadeMode(self, FadeCode : str = "Normal"):
        self.FadeCode = FadeCode

    def get_rect(self, position : int):
        return self.Rect[position+2]
    
    def check_Fadin_or_out(self, FadeMode : str):
        if FadeMode == "IN":
            return self.Alpha == 255
        elif FadeMode == "OUT":
            return self.Alpha == 0
    
    def check_Alpha(self, alpha : int):
        return self.Data.get_alpha() == alpha

    # 画像の描画
    def draw(self, Screen :pygame.surface.Surface):

        if(self.Data != None):
            if(self.FadeCode != "Normal"):
                if self.FadeCode == "IN":
                    Alpha = 0
                elif self.FadeCode == "OUT":
                    Alpha = 255
                #Alpha = 0 if self.FadeCode=="IN" else 255
                Alpha = Fader.Fade(Screen, self.FadeCode, self.Data,self.Coordinate, Alpha)
                self.Data.set_alpha(Alpha)
                self.FadeCode = "Normal"
    
            Screen.blit(self.Data, dest=self.Coordinate, area=self.Rect)
            
# テキストウィンドウクラス
# 決め打ち♡　必要があれば拡張性を増やす
class TextWindowPicture :
    # 初期化
    def __init__(self, gameFandamental : Game_Fandamental) :
        self.gameFandamental : Game_Fandamental = gameFandamental
        self.TextWindowData : pygame.surface.Surface = None
        self.LogButton : list[pygame.surface.Surface] = []
        self.AutoButton : list[pygame.surface.Surface] = []
        self.SaveButton : list[pygame.surface.Surface] = []
        self.LoadButton : list[pygame.surface.Surface] = []
        self.SettingButton : list[pygame.surface.Surface] = []
        self.TextWindowRect : pygame.Rect = None
        self.AutoButtonRect : pygame.Rect = None
        self.SaveButtonRect : pygame.Rect = None
        self.LoadButtonRect : pygame.Rect = None
        self.SettingButtonRect : pygame.Rect = None
        self.TextWindowCoor : tuple = None
        self.AutoButtonCoor : tuple = None
        self.SaveButtonCoor : tuple = None
        self.LoadButtonCoor : tuple = None
        self.SettingButtonCoor : tuple = None
        
        # 配列 0 : Auto, 1 : Save, 2 : Load, 3 : Setting
        self.OnCursol : list = []
        self.Swicher : str = "ON"
        self.isSwicher : bool = True

    def initialize(self):
        self.TextWindowData = self.gameFandamental.Data["Story"]["Picture"]["textwindow"]
        self.AutoButton.append(self.gameFandamental.Data["Story"]["Picture"]["autobuttonplay"]["0"])
        self.AutoButton.append(self.gameFandamental.Data["Story"]["Picture"]["autobuttonplay"]["1"])
        self.SaveButton.append(self.gameFandamental.Data["Story"]["Picture"]["savebutton"]["0"])
        self.SaveButton.append(self.gameFandamental.Data["Story"]["Picture"]["savebutton"]["1"])
        self.LoadButton.append(self.gameFandamental.Data["Story"]["Picture"]["loadbutton"]["0"])
        self.LoadButton.append(self.gameFandamental.Data["Story"]["Picture"]["loadbutton"]["1"])
        self.SettingButton.append(self.gameFandamental.Data["Story"]["Picture"]["Setting"]["0"])
        self.SettingButton.append(self.gameFandamental.Data["Story"]["Picture"]["Setting"]["1"])
        self.LogButton.append(self.gameFandamental.Data["Story"]["Picture"]["Logbutton"]["0"])
        self.LogButton.append(self.gameFandamental.Data["Story"]["Picture"]["Logbutton"]["1"])
        self.LogButtonRect = self.LogButton[0].get_rect()
        self.TextWindowRect = self.TextWindowData.get_rect()
        self.AutoButtonRect = self.AutoButton[0].get_rect()
        self.SaveButtonRect = self.SaveButton[0].get_rect()
        self.LoadButtonRect = self.LoadButton[0].get_rect()
        self.SettingButtonRect = self.SettingButton[0].get_rect()
        self.TextWindowCoor = (40,500)
        self.AutoButtonCoor = (self.gameFandamental.Data["Story"]["Picture"]["autobuttonplay"]["x"],
                               self.gameFandamental.Data["Story"]["Picture"]["autobuttonplay"]["y"])
        self.SaveButtonCoor = (self.gameFandamental.Data["Story"]["Picture"]["savebutton"]["x"],
                               self.gameFandamental.Data["Story"]["Picture"]["savebutton"]["y"])
        self.LoadButtonCoor = (self.gameFandamental.Data["Story"]["Picture"]["loadbutton"]["x"],
                               self.gameFandamental.Data["Story"]["Picture"]["loadbutton"]["y"])
        self.LogButtonCoor = (self.gameFandamental.Data["Story"]["Picture"]["Logbutton"]["x"],
                              self.gameFandamental.Data["Story"]["Picture"]["Logbutton"]["y"])
        self.SettingButtonCoor = (self.gameFandamental.Data["Story"]["Picture"]["Setting"]["x"],
                                  self.gameFandamental.Data["Story"]["Picture"]["Setting"]["y"])

        for i in range(5):
            self.OnCursol.append(0)
        self.Swicher : str = "OFF"

    # 表示のオンオフの切り替え
    def change_Display(self, OnOff : str = "OFF"):
        self.Swicher = OnOff
        self.isSwicher = self.isSwicher ^ True

    def OnTheCusol(self, ButtonName : str, value : int = 0):
        if(ButtonName == "Auto"):
            self.OnCursol[0] = self.OnCursol[0] ^ 1
        elif(ButtonName == "Save"):
            self.OnCursol[1] = value
            self.OnCursol[2] = not(value)
            self.OnCursol[3] = not(value)
            self.OnCursol[4] = not(value)
        elif(ButtonName == "Load"):
            self.OnCursol[1] = not(value)
            self.OnCursol[2] = value
            self.OnCursol[3] = not(value)
            self.OnCursol[4] = not(value)
        elif(ButtonName == "TextLog"):
            self.OnCursol[1] = not(value)
            self.OnCursol[2] = not(value)
            self.OnCursol[3] = not(value)
            self.OnCursol[4] = value
        elif(ButtonName == "Setting"):
            self.OnCursol[1] = not(value)
            self.OnCursol[2] = not(value)
            self.OnCursol[3] = value
            self.OnCursol[4] = not(value)

    def clear_OnTheCusol(self):
        self.OnCursol[1] = 0
        self.OnCursol[2] = 0
        self.OnCursol[3] = 0
        self.OnCursol[4] = 0

    # 描画
    def draw(self, Screen :pygame.surface.Surface):
        if(self.Swicher == "ON" or self.isSwicher):
            Screen.blit(self.TextWindowData, dest=self.TextWindowCoor, area=self.TextWindowRect)
            
            
            Screen.blit(self.AutoButton[self.OnCursol[0]], dest=self.AutoButtonCoor, area=self.AutoButtonRect)
            Screen.blit(self.SaveButton[self.OnCursol[1]], dest=self.SaveButtonCoor, area=self.SaveButtonRect)
            Screen.blit(self.LoadButton[self.OnCursol[2]], dest=self.LoadButtonCoor, area=self.LoadButtonRect)
            Screen.blit(self.LogButton[self.OnCursol[4]], dest=self.LogButtonCoor, area=self.LogButtonRect)
            Screen.blit(self.SettingButton[self.OnCursol[3]], dest=self.SettingButtonCoor, area=self.SettingButtonRect)

# ネームプレートクラス
# 位置などは調整中
class NamePlatePicture :
    # 初期化
    def __init__(self) : 
        self.NamePlateData = None
        self.NamePlateRect = None
        self.NamePlatePosition = None
        self.isSwicher : bool = True

    # データの切り替え
    def Change_NamePlate(self, Picture_Data : pygame.surface.Surface, Position) :
        self.NamePlateData = Picture_Data
        self.NamePlateRect = self.NamePlateData.get_rect()
        if Position == "left":
            self.NamePlatePosition = (50,480)
        elif Position == "middle":
            self.NamePlatePosition = (480, 480)
        elif Position == "right":
            self.NamePlatePosition = (1050,480)

    # 表示のオンオフの切り替え
    def change_Display(self, OnOff : str = "OFF"):
        self.isSwicher = self.isSwicher ^ True
    
    def clear_NamePlate(self):
        self.NamePlateData = None
        self.NamePlateRect = None
        self.NamePlatePosition = None

    # 描画
    def draw(self, Screen : pygame.surface.Surface):
        if(self.isSwicher):
            if(self.NamePlateData != None):
                Screen.blit(self.NamePlateData, dest=self.NamePlatePosition, area=self.NamePlateRect)

class Multiple_Picture:
    # 初期化
    def __init__(self):
        #self.Pictuer_Order : list = []
        self.Data : list = []
        self.Rect : list = []
        self.Coordinate : list = []
        self.Alpha : list = []
        self.FadeCodelist : list = []
        self.Name : list = []

    def clear_Picture(self):
        self.Data = []
        self.Rect = []
        self.Coordinate = []
        self.Alpha = []
        self.FadeCodelist = []
        self.Name : list = []

    # 表示画像登録関数
    # 過去の登録の有無に限らず一旦画像を消して
    # 再登録させる。
    def Regist_order_Picture(self, Picture_Name: list[str], Picture_Data : pygame.surface.Surface, Position : list[str], offset : tuple = (0,0), Fadecode :str = "Normal") :
        
        pict_height = Picture_Data.get_height()
        pict_width = Picture_Data.get_width()
        self.Data.append(Picture_Data)
        self.Rect.append(Picture_Data.get_rect())
        self.FadeCodelist.append(Fadecode)
        if Fadecode == "IN":
            self.Alpha.append(0)
        else :
             self.Alpha.append(255)
        pict_width += offset[0]
        pict_height += offset[1]

        if Position == "left":
            self.Coordinate.append((280-pict_width//2,1380-pict_height))
        elif Position == "m_left":
            self.Coordinate.append((460-pict_width//2,1380-pict_height))
        elif Position == "middle":
            self.Coordinate.append((640-pict_width//2, 1380-pict_height))
        elif Position == "m_right":
            self.Coordinate.append((820-pict_width//2,1380-pict_height))
        elif Position == "right":
            self.Coordinate.append((1000-pict_width//2,1380-pict_height))

        self.Name.append(Picture_Name)

    def Regist_order_Pictures(self, Picture_Name: list[str], Picture_Data : pygame.surface.Surface, Position : tuple, Fadecode :str = "Normal") :
        
        if (Picture_Name == "None"):
            self.Data.append(Picture_Data)
            self.Alpha.append(0)
            self.Coordinate.append(Position)
            self.Rect.append(Picture_Data.get_rect())
            self.FadeCodelist.append(Fadecode)
            self.Name.append(Picture_Name)
        else:
            self.Data.append(Picture_Data)
            self.Rect.append(Picture_Data.get_rect())
            self.FadeCodelist.append(Fadecode)
            if Fadecode == "IN":
                self.Alpha.append(0)
            else :
                self.Alpha.append(255)

            self.Coordinate.append(Position)
            self.Name.append(Picture_Name)

    def get_Dict_Rect(self, Name :str, Position : int):
        i : int
        i = 0

        while(self.Name[i] != Name):
            i = i + 1
        
        rect = self.Rect[i]

        return rect[Position + 2]

    def Regist_Pictures(self, Picture_Name: list[str], Picture_Data : pygame.surface.Surface, Coordinate : tuple, Fadecode : str = "Normal"):
        self.Data.append(Picture_Data)
        self.Rect.append(Picture_Data.get_rect())
        self.Coordinate.append(Coordinate)
        self.Alpha.append(255)
        self.FadeCodelist.append(Fadecode)
        self.Name.append(Picture_Name)

    def change_Pictures(self, Picture_Name: list[str], Picture_Data : pygame.surface.Surface, Position : list[str], index : int, Fadecode :str = "Normal"):
        self.Data[index] = Picture_Data
        self.Coordinate[index] = Position
        self.Rect[index] = Picture_Data.get_rect()
        self.Alpha[index] = 255
        self.FadeCodelist[index] = Fadecode
        self.Name.append(Picture_Name)

    def change_Picture(self, Picture_Name: list[str], Picture_Data : pygame.surface.Surface, index : int, Fadecode :str = "Normal"):
        self.Data[index] = Picture_Data
        self.Rect[index] = Picture_Data.get_rect()
        self.Alpha[index] = 255
        self.FadeCodelist[index] = Fadecode
        self.Name.append(Picture_Name)

    # 画像の描画
    def draw(self, Screen :pygame.surface.Surface):
        if(len(self.Data) != 0):
            for i in reversed(range(len(self.Data))) :
                if self.FadeCodelist[i] != "Normal":
                    self.Alpha[i] = Fader.Fade(Screen, self.FadeCodelist[i], self.Data[i],self.Coordinate[i], self.Alpha[i])
                    self.Data[i].set_alpha(self.Alpha[i])
                    
                    self.FadeCodelist[i] = "Normal"
                Screen.blit(self.Data[i], dest=self.Coordinate[i], area=self.Rect[i])

    def draw_mult(self, Screen :pygame.surface.Surface, start: int):
        if(len(self.Data) != 0):
            for i in range(start, start + 4, 1) :
                #if self.FadeCodelist[i] != "Normal":
                    #self.Alpha[i] = Fader.Fade(Screen, self.FadeCodelist[i], self.Data[i],self.Coordinate[i], self.Alpha[i])
                self.Data[i].set_alpha(self.Alpha[i])
                    
                #self.FadeCodelist[i] = "Normal"
                Screen.blit(self.Data[i], dest=self.Coordinate[i], area=self.Rect[i])
    
    # 画像サイズの取得
    def get_Rect(self, Data_Num : int ,getPosizition : str):
        if getPosizition == "x":
            return self.Data[Data_Num].get_width()
        elif getPosizition == "y":
            return self.Data[Data_Num].get_height()
        else:
            return 0
    
    def set_alpha(self, alpha : int, index : int):
        self.Alpha[index] = alpha



class TextPicture :
    
    MAX_COL = 35 # 1行の最大文字数
    MAX_ROW = 3 # 1回の表示で表示できる最大行数

    def __init__(self, gameFandamental : Game_Fandamental):
        self.font_kinds = gameFandamental.Data["Font"]["Data"]
        self.TextData : list[pygame.surface.Surface] = []
        self.TextRect : list[pygame.rect.Rect] = []
        self.TextCoor : list[tuple] = []
        self.isSwicher : bool = True

    def set_font(self, font_dir:list[str], font_size) :
        self.font_kinds = pygame.font.Font(font_dir, font_size)

    def set_Text_Picture(self, text:list[str]):
        self.TextData = []
        self.TextRect = []
        self.TextCoor = []
        text_index = 0
        x = 0
        y = 0
        while text_index < len(text):
            if text_index + 2 < len(text):
                if (text[text_index] == "/") & (text[text_index+1] == "b") & (text[text_index+2] == "r"):
                    y += 1
                    x = 0
                    text_index = text_index + 3
            
            self.TextData.append(self.font_kinds.render(text[text_index], True, (0,0,0)))
            self.TextRect.append(self.TextData[-1].get_rect())
            self.TextCoor.append((60+32*x, 520+47*y))

            text_index += 1
            x += 1

            if x % TextPicture.MAX_COL == 0 : 
                y += 1
                x = 0
    
    def undisplay_text(self):
        self.isSwicher = self.isSwicher ^ True

    def draw(self, Screen : pygame.surface.Surface):
        if(self.isSwicher):
            if(len(self.TextData) != 0):
                for i in range(len(self.TextData)) :
                    Screen.blit(self.TextData[i], dest=self.TextCoor[i], area=self.TextRect[i])

class TextOnePicture :
    
    def __init__(self, gameFandamental : Game_Fandamental):
        self.font_kinds = gameFandamental.Data["Font"]["Data"]
        self.TextData : pygame.surface.Surface = None
        self.TextRect : pygame.rect.Rect = None
        self.TextCoor : tuple = None

    def set_font(self, font_dir:list[str], font_size) :
        self.font_kinds = pygame.font.Font(font_dir, font_size)

    def set_Text_Picture(self, text:list[str]):
        self.TextData = None
        self.TextRect = None
        self.TextCoor = None
        text_index = 0
        x = 0
        y = 0
        while text_index < len(text):
            if text_index + 2 < len(text):
                if (text[text_index] == "/") & (text[text_index+1] == "b") & (text[text_index+2] == "r"):
                    y += 1
                    x = 0
                    text_index = text_index + 3
            
            self.TextData.append(self.font_kinds.render(text[text_index], True, (0,0,0)))
            self.TextRect.append(self.TextData[-1].get_rect())
            self.TextCoor.append((60+32*x, 520+47*y))

            text_index += 1
            x += 1

            if x % TextPicture.MAX_COL == 0 : 
                y += 1
                x = 0
        
    def draw(self, Screen : pygame.surface.Surface):
        if(len(self.TextData) != 0):
            for i in range(len(self.TextData)) :
                Screen.blit(self.TextData[i], dest=self.TextCoor[i], area=self.TextRect[i])


class GameSound :
    CurrentVoice = None

    # def __init__(self, game_config : dict ,file_dir : dict):
    def __init__(self, gameFandamental : Game_Fandamental):
        #self.game_config : dict = game_config
        #self.file_dir : dict = file_dir
        self.gameFandamental : Game_Fandamental = gameFandamental
        self.BGM_Channel = pygame.mixer.Channel(0)
        self.Voice_Channel = pygame.mixer.Channel(1)
        self.Effect_Channel = pygame.mixer.Channel(2)
        self.Voice_Data = None

    def start_BGM(self, BGMData : object):
        if not self.BGM_Channel.get_busy():
            self.BGM_Channel.set_volume(self.gameFandamental.Data["Setting"]["Sound"][self.gameFandamental.Config["SoundVolume"]]["value"])
            self.BGM_Channel.play(self.gameFandamental.Data["Story"]["Sound"][BGMData], -1)
    
    def busy(self):
        if self.BGM_Channel.get_busy():
            return True
        
        return False

    def stop_BGM(self):
        if self.BGM_Channel.get_busy():
            self.BGM_Channel.stop()

    
    def fadeout_BGM(self, time : float):
        if self.BGM_Channel.get_busy():
            self.BGM_Channel.fadeout(time)

    def start_EffectSound(self, EffectData : object):
        if not self.Effect_Channel.get_busy():
            self.Effect_Channel.set_volume(self.gameFandamental.Config["EffectVolume"])
            self.Effect_Channel.play(EffectData)

    def stop_EffectSound(self):
        if self.Effect_Channel.get_busy():
            self.Effect_Channel.stop()

    def Regist_Voice(self, VoiceData : str):
        #self.Voice_Data = pygame.mixer.Sound(VoiceData)
        self.Voice_Data = self.gameFandamental.Data["Story"]["Sound"][VoiceData]

    def voice_play(self):
        if self.Voice_Data != self.CurrentVoice:
            self.Voice_Channel.set_volume(self.gameFandamental.Data["Setting"]["Sound"][self.gameFandamental.Config["VoiceVolume"]]["value"])
            self.Voice_Channel.play(self.Voice_Data)
            self.CurrentVoice = self.Voice_Data

    def voice_Stop(self):
        if self.Voice_Channel.get_busy():
            self.Voice_Channel.stop()
            self.Voice_Data = None

    def update_Volume(self):
        self.BGM_Channel.set_volume(self.gameFandamental.Data["Setting"]["Sound"][self.gameFandamental.Config["SoundVolume"]]["value"])
        self.Voice_Channel.set_volume(self.gameFandamental.Data["Setting"]["Sound"][self.gameFandamental.Config["VoiceVolume"]]["value"])

    def set_BGM_Volume(self, volume : float):
        self.BGM_Channel.set_volume(volume)

    def set_Voice_Volume(self, volume : float):
        self.Voice_Channel.set_volume(volume)

class Fader:
    def Fade(Screen :pygame.Surface, state : str , picture : pygame.Surface, Coordinate : tuple, Alpha : int):
        clock = pygame.time.Clock()
        running = True

        screen_copy = Screen.copy()

        while running :
            for event in pygame.event.get():
                if(event.type == pygame.MOUSEBUTTONUP):
                    if state == "IN":
                        Alpha = 255
                    elif state == "OUT":
                        Alpha = 0
            
            Screen.blit(screen_copy, (0,0))

            # フェードイン処理
            if state == "IN":
                if Alpha < 255:
                    Alpha = min(Alpha + 5, 255)
                else:
                    running = False # フェードイン完了
            # フェードアウト処理
            elif state == "OUT":
                if Alpha > 0:
                    Alpha = max(Alpha-5, 0)
                else:
                    running = False # フェードアウト完了
            
            # アルファ値を適用して画像を描画
            picture.set_alpha(Alpha)
            Screen.blit(picture, Coordinate)

            # 描画処理
            pygame.display.update()
            clock.tick(30)

        return Alpha
    
class Timer : 
    def __init__(self):
        self.Now_Time : float = 0
        self.finish_time : int = 0 #second
        self.totalTime : int = 0
        self.game_clock = pygame.time.Clock()
        self.OnOff : bool = False
        self.pouse : bool = False
        self.start : bool = False
        self.fps = 30

    def set_timer(self, finish_time : int):
        self.finish_time = finish_time
        self.totalTime = finish_time * 1000 # millisecond -> second

    def Turn_Timer(self):
        self.OnOff = self.OnOff ^ True 
        if self.OnOff :
            self.totalTime =  self.finish_time * 1000 # millisecond -> second
    
    def chenge_finish_time(self, finish_time : int):
        self.finish_time = finish_time

    def timer_start(self):
        self.game_clock.tick(self.fps)
        self.start = self.game_clock.get_time()
        self.OnOff = True

    def stop_Timer(self):
        self.OnOff = False
        self.totalTime = self.finish_time * 1000

    def pouse_Timer(self):
        self.pouse = True

    def restart_Timer(self):
        self.pouse = False

    def check_start(self):
        return self.OnOff
    
    def check_pouse(self):
        return self.pouse
    
    def check_finish_time(self, finish_time : int):
        return self.finish_time == finish_time

    def update(self):
        if(self.OnOff and not(self.pouse)):
            self.game_clock.tick(self.fps)
            self.Now_Time = self.game_clock.get_time()
            self.totalTime = max(self.totalTime - self.Now_Time, 0)
        if("debugpy" in sys.modules):
            print("totalTime : %d" % self.totalTime)
        
    def check_time(self):
        if(self.totalTime <= 0): # millisecond -> second
            self.totalTime = self.finish_time * 1000 # 再設定
            # この時ONにする
            return True
        else:
            # この時OFFにする
            return False
        
    def reset(self):
        self.totalTime = self.finish_time * 1000

class Screen_Manager:
    #def __init__(self, game_config : dict, file_dir : dict, screen : pygame.surface.Surface):
    def __init__(self, gameFandamental : Game_Fandamental, screen : pygame.surface.Surface):
        # すべてをイニシャライズ
        #self.game_config = game_config
        #self.file_dir = file_dir
        self.gameFandamental : Game_Fandamental = gameFandamental
        self.Screen : pygame.surface.Surface = screen
        self.BackGround : BackgroundPicture = BackgroundPicture()
        self.Charactor : Multiple_Picture = Multiple_Picture()
        self.TextWindow : TextWindowPicture = TextWindowPicture(self.gameFandamental)
        self.Nameplate : NamePlatePicture = NamePlatePicture()
        self.Text : TextPicture = TextPicture(self.gameFandamental)
        self.GameSoundData : GameSound = GameSound(self.gameFandamental)
        self.isTextWindow : bool =  True

        self.TextWindow.initialize()

    def Register_ScreenInfo(self, Picture_Dictionary : BasePicture, ScreenInfo : dict):
        # 辞書型の変数内にキーワードが存在しているかを確認しつつ
        # 存在した場合に画像登録を行う。
        if "background" in ScreenInfo:
            word = ScreenInfo["background"]["Data"]
            if "Fade" in ScreenInfo["background"]:
                Fade = ScreenInfo["background"]["Fade"]
                self.BackGround.Regist_order_Picture(word, 
                                                     self.gameFandamental.Data["Story"]["Picture"][word],
                                                     (0, 0), 
                                                     Fade)
                #self.BackGround.Regist_order_Picture(word, Picture_Dictionary.get_Picture_Data(word), (0, 0), Fade)
            else:
                self.BackGround.Regist_order_Picture(word, 
                                                     self.gameFandamental.Data["Story"]["Picture"][word],
                                                     (0, 0))
                #self.BackGround.Regist_order_Picture(word, Picture_Dictionary.get_Picture_Data(word), (0, 0)) 
            self.gameFandamental.Data["tmp_Save"]["BackGround"]["Data"] = word
            #self.gameFandamental.Data["tmp_Save"]["BackGround"]["Name"] = word
        
        if "Charactor" in ScreenInfo:
            self.Charactor.clear_Picture()
            Total_Charactor = ScreenInfo["Charactor"]["Total_Charactor"]
            if Total_Charactor > 0:
                Charactor = ScreenInfo["Charactor"]
                for Charactor_Number in range(1,Total_Charactor+1, 1):
                    Now_Load_Charactor = "Charactor" + str(Charactor_Number)
                    word = Charactor[Now_Load_Charactor]["Data"]
                    position = Charactor[Now_Load_Charactor]["Position"]
                    if "tamaki" in word:
                        offset = (self.gameFandamental.Config["tamaki"]["width_Offset"], self.gameFandamental.Config["tamaki"]["height_Offset"])
                    elif "sizuku" in word:
                        offset = (self.gameFandamental.Config["sizuku"]["width_Offset"], self.gameFandamental.Config["sizuku"]["height_Offset"])
                    elif "mio" in word:
                        offset = (self.gameFandamental.Config["mio"]["width_Offset"], self.gameFandamental.Config["mio"]["height_Offset"])

                    if "Fade" in Charactor[Now_Load_Charactor]:
                        Fade = Charactor[Now_Load_Charactor]["Fade"]
                        self.Charactor.Regist_order_Picture(word, 
                                                            self.gameFandamental.Data["Story"]["Picture"][word], 
                                                            position, 
                                                            offset, 
                                                            Fade)
                    else:
                        self.Charactor.Regist_order_Picture(word, 
                                                            self.gameFandamental.Data["Story"]["Picture"][word], 
                                                            position, 
                                                            offset)

        if "TextWindow" in ScreenInfo:
            self.TextWindow.change_Display(ScreenInfo["TextWindow"])

        if "message" in ScreenInfo:
            word = ScreenInfo["message"]["text"]
            self.Text.set_Text_Picture(word)
            if "name" in ScreenInfo["message"]:
                Plate = ScreenInfo["message"]["name"]
                if "position" in ScreenInfo["message"]:
                    Plate_Position = ScreenInfo["message"]["position"]
                else :
                    Plate_Position = "left"
                self.Nameplate.Change_NamePlate(self.gameFandamental.Data["Story"]["Picture"][Plate], 
                                                Plate_Position)
            else:
                self.Nameplate.clear_NamePlate()

            if "voice" in ScreenInfo["message"]:
                voice = ScreenInfo["message"]["voice"]
                self.GameSoundData.Regist_Voice(voice)
            else:
                self.GameSoundData.voice_Stop()

        if 'BGM' in ScreenInfo.keys():
            BGM = ScreenInfo['BGM']
            self.gameFandamental.Data["tmp_Save"]["BGM"] = BGM
            self.GameSoundData.start_BGM(BGM)
            

        if 'stop_BGM' in ScreenInfo.keys():
            self.GameSoundData.stop_BGM()
            self.gameFandamental.Data["tmp_Save"]["BGM"] = ""

        if 'SE' in ScreenInfo.keys():
            SE = ScreenInfo['SE']
            self.GameSoundData.start_EffectSound(SE)

        if 'stop_SE' in ScreenInfo.keys():
            self.GameSoundData.stop_EffectSound()
        
        return
    
    def undisplay_textwindow(self):
        self.TextWindow.change_Display()
        self.Nameplate.change_Display()
        self.Text.undisplay_text()

    def save_image(self):
        pygame.image.save(self.Screen,"./Data/save/tmp.png")
    
    def draw(self):
        self.BackGround.draw(self.Screen)
        self.Charactor.draw(self.Screen)
        
        self.GameSoundData.voice_play()


        # テキストウィンドウをオンオフ機能
        if self.TextWindow :
            self.TextWindow.draw(self.Screen)
            self.Nameplate.draw(self.Screen)
            self.Text.draw(self.Screen)

    def set_Background(self, Name : str):
        self.BackGround.Regist_order_Picture(Name, 
                                            self.gameFandamental.Data["Story"]["Picture"][Name],
                                            (0, 0), 
                                            )
    
    def change_SystemButton(self, ButtonName : str, value : int = 0):
        if ButtonName == "Clear":
            self.TextWindow.clear_OnTheCusol()
            return
        
        self.TextWindow.OnTheCusol(ButtonName, value)
    


# 自作関数
def MessageForeFront(Title : str, Message :str):
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    root.withdraw()
    ret = messagebox.askyesno(Title, Message)

    root.destroy()

    pygame.display.init()
    return ret

def MessageForefrontShowinfo(Title : str, Message :str):
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    root.withdraw()
    ret = messagebox.showinfo(Title, Message)

    root.destroy()
    pygame.display.init()

def MessageForefrontShowwarning(Title : str, Message :str):
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    root.withdraw()
    ret = messagebox.showwarning(Title, Message)

    root.destroy()
    pygame.display.init()

def file_decryped(file : str, key : str = "AdDM0FwpT5LhQmhzMDaa78Z0VlzdOT6SFJTS_gnbS48="):
    
    fernet = Fernet(key)

    # 暗号化されたファイルを読み込み
    #with open(file , 'rb') as file :
    #    encrypted = file.read()
    
    decrypted = fernet.decrypt(file)

    return decrypted

def file_encryped(file : str, key : str = "AdDM0FwpT5LhQmhzMDaa78Z0VlzdOT6SFJTS_gnbS48="):
    
    fernet = Fernet(key)

    # 暗号化されたファイルを読み込み
    #with open(file , 'rb') as file :
    #    encrypted = file.read()
    
    encryped = fernet.encrypt(file)

    return encryped