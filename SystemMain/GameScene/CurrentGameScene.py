from enum import Enum

class CurrentGameScene(Enum):
    NONE_SCENE = 0
    TITLE_SCENE = 1
    INTRO = 100
    LOAD = 800
    SETTING = 801
    GAMEMENU = 802
    SAVE = 803
    AUTO = 804
    GALLERY = 805
    DRAWCG = 806
    TEXTLOG = 807
    QUIT = 900
    RETURN = 1000
    CG1 = 1101
    CG201 = 1102
    CG202 = 1103
    CG3 = 1104
    CG4 = 1105
    CG5 = 1106
    CG6 = 1107
    CG7 = 1108
    CG8 = 1109
    CG9 = 1110
    CG10 = 1111
    CG11 = 1112
    CG12 = 1113
    CG13 = 1114
    CG14 = 1115
    CG15 = 1116
    CG16 = 1117
    CG17 = 1118
    CG18 = 1119
    CG19 = 1120
    CG20 = 1121
    CG21 = 1122
    CG22 = 1123
    CG23 = 1124
    ENDING = 2000

class NextGameOperation(Enum):
    NONE = 0
    GOTOSAVE = 100
    GOTOLOAD = 200
    GOTOTitle = 300
    RETURNTOPREVIEW = 400
    CHENGEAUTO = 500
    CHENGEVOICE = 600
    CHENGESOUND = 700
    CHENGEDISPLAY = 800
    

class CurrentTitleStatus(Enum):
    WAIT_TIME = 0 # 入力待ち状態(待機状態)
    TRANSITION_STATE = 100 # 遷移状態(次のシーンに移行するための準備状態)
    GOTO_NEXT_SCENE = 200 # 次のシーンに飛ぶ

class CurrentGameStatus(Enum):
    WAITTING = 100  # 読んでない状態（文面を表示しているか、何も表示されていない状態、今後状態を分けるかも）
    READING = 200   # 読み発生状態 (文面表示中)
    LOADING = 300   # データ読み込み中

class LoadState(Enum):
    RETRUN = 100
    NEXTTOSAVEDATA = 200
    PREVIEWTOSAVEDATA = 300
    LOAD = 400

class SaveState(Enum):
    RETRUN = 100
    NEXTTOSAVEDATA = 200
    PREVIEWTOSAVEDATA = 300
    SAVE = 400

class GameState(Enum):
    NORMAL = 1
    SCENE_FADEOUT = 100
    SCENE_FADEIN = 200
