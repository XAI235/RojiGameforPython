
import os,sys
from SystemMain import SystemMain
#os.path.abspath(__file__) : pythonファイルが存在する絶対パスを取得
#os.path.dirname(): 入力したパスの一つ上の階層のパスを取得

ROOTPATH = os.path.dirname(os.path.abspath(__file__))
CFGPATH = os.path.dirname(os.path.dirname(ROOTPATH))

#sys.path.append() ：入力したパスをpythonファイルの探索パスに追加する

sys.path.append(CFGPATH)

def main():
        SysM = SystemMain.SystemMain()

        if(SysM.initialize(1280, 720,'1280x720','ぼくらの時間')) :
                SysM.systemmain()

        SysM.finalize()
        return 0


if __name__ == "__main__":
        main()