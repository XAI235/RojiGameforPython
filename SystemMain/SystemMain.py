import tkinter

class SystemMain:

    ScreenSize = None
    TitleName = None
    def __init__(self, screensize,titlename):
        self.frm = tkinter.Tk()
        self.ScreenSize = screensize
        self.TitlName = titlename
        return
    
    def __del__(self):
        return 

    def initialize(self):
        frm = tkinter.Tk()
        frm.geometry(self.ScreenSize)
        frm.title(self.TitleName)
        return True

    def systemMain():
        2+1

    def finalize():
        3+1