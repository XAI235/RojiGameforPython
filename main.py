from SystemMain import SystemMain

def main():
        SysM = SystemMain.SystemMain()

        if(SysM.initialize(1280, 720,'ぼくらの時間')) :
                SysM.systemmain()

        SysM.finalize()
        return 0


if __name__ == "__main__":
        main()