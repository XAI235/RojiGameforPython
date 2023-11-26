from SystemMain import SystemMain

def main():
        SysM = SystemMain.SystemMain()

        if(SysM.initialize()) :
                SysM.systemmain()

        SysM.finalize()
        return 0


if __name__ == "__main__":
        main()