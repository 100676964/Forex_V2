from tkinter import *
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from API import oanda
from GUI import login,registration,autotrade
class switch:
    def __init__(self,root:Tk,theme:dict) -> None:
        self.root = root
        self.theme = theme
        self.registration = registration.registration(root,theme,self)
        self.login = login.login(root,theme,self)
        self.login.canvas.grid(row=0,column=0,sticky='nsew')
    
    def access_bot(self,name,accountId,token):
        self.clear()
        self.API = oanda.OandaAPI(accountId,token,update=True)
        self.autotrade = autotrade.autotradeUI(self.root,self.theme,self,self.API)
        self.autotrade.canvas.grid(row=0,column=0,sticky='nsew')
        
    
    
    def go_to_login(self):
        self.clear()
        self.login.canvas.grid(row=0,column=0,sticky='nsew')
    
    def go_to_registration(self):
        self.clear()
        self.registration.canvas.grid(row=0,column=0,sticky='nsew')

    def clear(self):
        for child in self.root.winfo_children():
            child.grid_forget()