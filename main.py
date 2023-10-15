from SystemMain import SystemMain

def main():
        systemM = SystemMain('1280x720','ぼくらの時間')

        if(systemM.initialize()) :
                systemM.systemMain()

        systemM.finalize()
        return 0


if __name__ == "__main__":
        main()