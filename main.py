from SystemMain import SystemMain

def main():
        systemmain = SystemMain()

        if(systemmain.initialize()) :
                systemmain.systemMain()

        systemmain.finalize()
        return 0


if __name__ == "__main__":
        main()