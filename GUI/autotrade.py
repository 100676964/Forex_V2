from tkinter import *
import threading
import time
import os, sys
import traceback
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from GUI import plot
from API import oanda
from Trade import trade
class autotradeUI:
    def __init__(self,root:Tk,theme:dict,switch,API:oanda.OandaAPI) -> None:
        self.API = API
        self.current_pair = 0
        self.closing_rates = []
        self.position = []

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
        # self.graphcanvas_1.grid(row = 2, rowspan = 2, column = 1, sticky = "nsew")
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

        #........................................................................Pair selection............................................................
        self.selectioncanvas = Canvas(self.canvas,background = "grey",highlightthickness=0)
        self.selectioncanvas.grid(row = 2, column = 2,pady = 5)
        
        scrollbar = Scrollbar(self.selectioncanvas,background=theme.get('widgetBgColor'))
        scrollbar.pack(side=RIGHT,fill=Y)
        
        self.listbox = Listbox(self.selectioncanvas,
                                background=theme.get('widgetBgColor'),
                                font=('Arial',25, 'bold'),
                                activestyle='none',
                                selectbackground=theme.get('pressedColor'),
                                justify=CENTER,
                                yscrollcommand=scrollbar.set)

        self.listbox.pack(side=LEFT,fill=BOTH)
        self.listbox.event_generate("<<ListboxSelect>>")
        scrollbar.config(command=self.listbox.yview)

    def graph_update(self):
        buffer = 0
        while True:
            try:
                position = None
                if len(self.position) > 0:
                    position = float(self.position[2])
                if self.canvas.winfo_viewable() == True and len(self.closing_rates) > 10:
                    if buffer == 0:
                        plot.plot(self.graphcanvas_1,self.closing_rates,position = position)
                        buffer = 1
                    elif buffer == 1:
                        plot.plot(self.graphcanvas_2,self.closing_rates,position = position)
                        buffer = 0
                time.sleep(0.1)
            except:
                traceback.print_exc()
    
    def data_update(self):
        while True:
            if self.canvas.winfo_viewable() == True and len(self.API.rates) != 0:
                
            #initial
                self.pairs = self.API.rates[:,0]

                self.closing_rates = self.to_floats(self.API.rates[:,1][self.current_pair][:,0][:,3]) 
                #check current selected pair
                if len(self.listbox.curselection()) > 0:
                    self.current_pair = self.listbox.curselection()[0]
                #get positions for current pair 
                all_positions = self.API.open_positions
                if all_positions is not None:
                    for p in all_positions:
                        if p[0] == self.API.rates[:,0][self.current_pair]:
                            self.position = p
                        else:
                            self.position = []
                else:
                    self.position = []
                
            #Trade



            #GUI updates    
                #update pair selection box
                if self.listbox.size() != len(self.pairs):
                    self.listbox.delete(0,END)
                    for i in range(len(self.pairs)):
                        self.listbox.insert(i,self.pairs[i])
                

            time.sleep(0.5)
    def OnMouseWheel(self,event):
        pass
    
    def to_floats(self,l):
        return [float(i) for i in l]
