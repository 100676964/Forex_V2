from tkinter import *
class login_gui:
    def __init__(self,root:Tk,api,theme) -> None:
        for child in root.winfo_children():
            child.destroy()
        pass