from tkinter import *
import threading
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from API import oanda
class autotradeUI:
    def __init__(self,root:Tk,theme:dict,switch,API:oanda.OandaAPI) -> None:
        self.API = API
        self.canvas = Canvas(root,background = theme.get('background_color'))
        self.canvas.rowconfigure(0,weight = 1)
        self.canvas.rowconfigure(1,weight = 0)
        self.canvas.rowconfigure(2,weight = 0)
        self.canvas.rowconfigure(3,weight = 3)
        self.canvas.rowconfigure(4,weight = 3)
        self.canvas.rowconfigure(5,weight = 0)
        self.canvas.rowconfigure(6,weight = 1)

        self.canvas.columnconfigure(0,weight = 1)
        self.canvas.columnconfigure(1,weight = 5)
        self.canvas.columnconfigure(2,weight = 0)
        self.canvas.columnconfigure(3,weight = 1)

        #........................................................................Page message...............................................................
        self.message = Label(self.canvas, text='Auto Trade', font = theme.get('labelFonts'), background = theme.get('widgetBgColor'))
        self.message.grid(row = 1, column = 1, columnspan = 2, sticky = 'ew')

        #........................................................................Graph......................................................................
        
        self.graphcanvas_1 = Canvas(self.canvas,background = theme.get('background_color'),highlightthickness=0)
        self.graphcanvas_1.grid(row = 2, rowspan = 2, column = 1, sticky = "nsew")
        self.graphcanvas_2 = Canvas(self.canvas,background = theme.get('background_color'),highlightthickness=0)
        
        self.graphcanvas_1.bind("<MouseWheel>",self.OnMouseWheel)
        self.graphcanvas_2.bind("<MouseWheel>",self.OnMouseWheel)
        self.plotlist = []
        t1 = threading.Thread(target = self.graph_update)
        t2 = threading.Thread(target = self.data_update)
        t1.daemon = True
        t2.daemon = True
        t1.start()
        t2.start()

    def graph_update(self):
        pass
    def data_update(self):
        pass
    
    def OnMouseWheel(self,event):
        pass
