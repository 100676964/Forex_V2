from tkinter import *
import threading
from datetime import datetime
import time
import os, sys
import traceback

from numpy.lib.function_base import average
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from GUI import plot
from API import oanda
from Trade import trade
class autotradeUI:
    def __init__(self,root:Tk,theme:dict,switch,API:oanda.OandaAPI) -> None:
        self.root = root
        self.API = API
        self.current_pair = 0
        self.closing_rates = []
        self.all_closing_rates = []
        self.position = []
        self.trading = False
        self.n_of_points = 30

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
        self.selectioncanvas.rowconfigure(0,weight = 0)
        self.selectioncanvas.columnconfigure(0,weight = 5)
        self.selectioncanvas.columnconfigure(1,weight = 1)
        self.selectioncanvas.grid(row = 2, column = 2,pady = 5)
        
        scrollbar = Scrollbar(self.selectioncanvas,background=theme.get('widgetBgColor'))
        scrollbar.grid(row = 0,column=1,sticky='ns')
        
        self.listbox = Listbox(self.selectioncanvas,
                                height=5,
                                background=theme.get('widgetBgColor'),
                                font=('Arial',25, 'bold'),
                                activestyle='none',
                                selectbackground=theme.get('pressedColor'),
                                justify=CENTER,
                                yscrollcommand=scrollbar.set)

        self.listbox.grid(row=0,column=0,sticky='ns')
        self.listbox.event_generate("<<ListboxSelect>>")
        scrollbar.config(command=self.listbox.yview)
        #.........................................................................pair_info.......................................................................
        self.pair_info = Canvas(self.canvas,background = 'gray',highlightthickness=0)
        self.pair_info.grid(row = 3, column = 2, sticky = 'nsew',pady = 5)
        self.pair_info.rowconfigure(0, weight = 0)
        self.pair_info.rowconfigure(1, weight = 0)
        self.pair_info.rowconfigure(2, weight = 0)
        self.pair_info.rowconfigure(3, weight = 1)
        self.pair_info.rowconfigure(4, weight = 0)
        self.pair_info.rowconfigure(5, weight = 1)

        self.pair_info.columnconfigure(0,weight = 1)
        #row 1
        Label(self.pair_info, text='Profit/Loss', font = theme.get('labelFonts'), background = theme.get('widgetBgColor')).grid(row = 0, column = 0, sticky = 'ew',padx = 5,pady = (5,0))
        self.pair_pl = Label(self.pair_info, text='', font = theme.get('labelFonts'), background = theme.get('widgetBgColor'))
        self.pair_pl.grid(row = 1, column = 0, sticky = 'nsew',padx = 5,pady = (0,5))
        
        #row 2
        Label(self.pair_info, text='Position Value', font = theme.get('labelFonts'), background = theme.get('widgetBgColor')).grid(row = 2, column = 0, sticky = 'ew',padx = 5,pady = (5,0))
        self.pair_value = Label(self.pair_info, text='', font = theme.get('labelFonts'), background = theme.get('widgetBgColor'))
        self.pair_value.grid(row = 3, column = 0, sticky = 'nsew',padx = 5,pady = (0,5))

        #row 3
        Label(self.pair_info, text='Holdings', font = theme.get('labelFonts'), background = theme.get('widgetBgColor')).grid(row = 4, column = 0, sticky = 'ew',padx = 5,pady = (5,0))
        self.pair_holdings = Label(self.pair_info, text='', font = theme.get('labelFonts'), background = theme.get('widgetBgColor'))
        self.pair_holdings.grid(row = 5, column = 0, sticky = 'nsew',padx = 5,pady = (0,5))
        
        #.........................................................................General_Info.......................................................................
        self.general_info = Canvas(self.canvas,background = 'gray',highlightthickness=0)
        self.general_info.grid(row = 4, column = 1, columnspan = 2, sticky = 'nsew',pady = 5)
        self.general_info.rowconfigure(0,weight = 1)
        self.general_info.rowconfigure(1,weight = 1)
        self.general_info.columnconfigure(0,weight = 1)
        self.general_info.columnconfigure(1,weight = 1)
        self.general_info.columnconfigure(2,weight = 1)
        self.general_info.columnconfigure(3,weight = 1)
        #row 1
        Label(self.general_info, text='Total Worth:', font = theme.get('labelFonts'), background = theme.get('widgetBgColor')).grid(row = 0, column = 0, sticky = 'nsew', padx = (5,0), pady = 5)
        self.total_worth = Label(self.general_info, text='', font = theme.get('labelFonts'), background = theme.get('widgetBgColor'))
        self.total_worth.grid(row = 0, column = 1, sticky = 'nsew',padx = (0,5) ,pady = 5)

        Label(self.general_info, text='Total Profit/Loss:', font = theme.get('labelFonts'), background = theme.get('widgetBgColor')).grid(row = 0, column = 2, sticky = 'nsew', padx = (5,0), pady = 5)
        self.total_pl_entry = Label(self.general_info, text='', font = theme.get('labelFonts'), background = theme.get('widgetBgColor'))
        self.total_pl_entry.grid(row = 0, column = 3, sticky = 'nsew',padx = (0,5) ,pady = 5)
        #row 2
        Label(self.general_info, text='Total Cash:', font = theme.get('labelFonts'), background = theme.get('widgetBgColor')).grid(row = 1, column = 0, sticky = 'nsew', padx = (5,0), pady = 5)
        self.total_cash = Label(self.general_info, text='', font = theme.get('labelFonts'), background = theme.get('widgetBgColor'))
        self.total_cash.grid(row = 1, column = 1, sticky = 'nsew',padx = (0,5) ,pady = 5)

        Label(self.general_info, text='Positons Value:', font = theme.get('labelFonts'), background = theme.get('widgetBgColor')).grid(row = 1, column = 2, sticky = 'nsew', padx = (5,0), pady = 5)
        self.total_p_value = Label(self.general_info, text='', font = theme.get('labelFonts'), background = theme.get('widgetBgColor'))
        self.total_p_value.grid(row = 1, column = 3, sticky = 'nsew',padx = (0,5) ,pady = 5)
        
        #.........................................................................Auto Trading Toggle.................................................................
        self.btn_Canvas = Canvas(self.canvas,background = 'gray',highlightthickness=0)
        self.btn_Canvas.grid(row = 5, column = 1, columnspan = 2,sticky = 'nsew',pady = 10)
        self.btn_Canvas.rowconfigure(0,weight = 1)
        self.btn_Canvas.columnconfigure(0,weight = 1)

        self.btn_trade_start = Button(
            self.btn_Canvas, 
            text="Start Auto Trade", 
            font = theme.get('buttonFonts'), 
            width = 20, 
            height = 2, 
            background = theme.get('widgetBgColor'), 
            activebackground = theme.get('pressedColor'),
            command = lambda: self.start_stop_toggle(True)
            )
        self.btn_trade_start.grid(row = 0, column = 0, sticky = "nsew", padx = 10, pady = 10)

        self.btn_trade_stop = Button(
            self.btn_Canvas, 
            text="Stop Auto Trade", 
            font = theme.get('buttonFonts'), 
            width = 20, 
            height = 2, 
            background = theme.get('widgetBgColor'), 
            activebackground = theme.get('pressedColor'),
            command = lambda: self.start_stop_toggle(False)
            )

    def graph_update(self):
        buffer = 0
        while True:
            try:
                position = None
                parameters = None
                if len(self.position) > 0:
                    position = float(self.position[2])
                if len(self.closing_rates) > 50:
                    parameters = trade.calculate_bands(self.closing_rates)
                if self.canvas.winfo_viewable() == True and len(self.closing_rates) > 10:
                    if buffer == 0:
                        plot.plot(self.graphcanvas_1,self.closing_rates[-self.n_of_points:],position = position,parameters=parameters)
                        buffer = 1
                    elif buffer == 1:
                        plot.plot(self.graphcanvas_2,self.closing_rates[-self.n_of_points:],position = position,parameters=parameters)
                        buffer = 0
                time.sleep(0.1)
            except:
                traceback.print_exc()
    
    def data_update(self):
        while True:
            if len(self.API.rates) != 0 and len(self.API.acct_info) != 0: 
            #initial..............................
                self.pairs = self.API.rates[:,0]

                self.closing_rates = self.to_floats(self.API.rates[:,1][self.current_pair][:,0][:,3])
                for i in range(len(self.pairs)):
                    self.all_closing_rates.append(self.to_floats(self.API.rates[:,1][i][:,0][:,3]))
                #check current selected pair for display
                if len(self.listbox.curselection()) > 0:
                    self.current_pair = self.listbox.curselection()[0]
                #get positions for current pair 
                self.all_positions = self.API.open_positions
                if len(self.all_positions) > 0:
                    for p in self.all_positions:
                        if p[0] == self.API.rates[:,0][self.current_pair]:
                            self.position = p
                        else:
                            self.position = []
                else:
                    self.position = []

                #get accountinformation
                self.acct_info = self.to_floats(self.API.acct_info)
                self.NAV = self.acct_info[0]
                self.total_PL = self.acct_info[1]+self.acct_info[3]
                self.avaliableMargin = self.acct_info[2]
                self.total_positon_value = self.acct_info[4]
                
            #Trade................................
                if self.trading == True:
                    immediate_position_update = False
                    buy_list,sell_list = trade.get_actions(self.API.rates[:,0],self.all_closing_rates,self.NAV,self.avaliableMargin,self.all_positions)
                    if len(buy_list) > 0:
                        prices = self.API.get_price(buy_list[:,0])
                        print(prices)
                        for i in range(len(buy_list)):
                            
                            self.API.make_order(buy_list[i][0],str(int(float(buy_list[i][1])/(float(prices[i][1])*float(prices[i][2])))))
                            print('buy',buy_list[i][0],float(buy_list[i][1])/(float(prices[i][1])*float(prices[i][2])))
                        immediate_position_update == True
                    
                    if len(sell_list) > 0:
                        for sell in sell_list:
                            # self.API.make_order(sell[0].replace('/','_'),str(sell[1]))
                            
                            print('sell',sell[0],str(sell[1]))
                        immediate_position_update == True

                    if immediate_position_update == True:
                            self.API.open_positions = self.API.get_open_positions()
                            while True:
                                if len(self.API.open_positions) > 0:
                                    if self.all_positions.shape == self.API.open_positions.shape:
                                        if (self.all_positions == self.API.open_positions).all():
                                            print("De-sync error")
                                        else:
                                            break
                                    else:
                                        break
                                else:
                                    print("No Connection")
                                self.API.open_positions = self.API.get_open_positions()
                                time.sleep(1)
                                    
                            immediate_position_update = False
            
            #GUI updates..........................
                if self.canvas.winfo_viewable() == True:    
                    #update pair selection box
                    if self.listbox.size() != len(self.pairs):
                        self.listbox.delete(0,END)
                        for i in range(len(self.pairs)):
                            self.listbox.insert(i,self.pairs[i])
                        self.listbox.select_set(0)
                        
                    if len(self.position) > 0:
                        self.pair_pl.config(text = "C$ "+str(self.position[3]))
                        self.pair_value.config(text = "C$ "+str(self.position[4]))
                        self.pair_holdings.config(text = str(int(self.position[1]))+" pips")
                    else:
                        self.pair_pl.config(text = "C$ 0")
                        self.pair_value.config(text = "C$ 0")
                        self.pair_holdings.config(text = "0 pips")

                    self.total_worth.config(text = "C$ "+str(round(self.NAV,2)))
                    self.total_pl_entry.config(text = "C$ "+str(round(self.total_PL,2)))
                    self.total_cash.config(text = "C$ "+str(round(self.avaliableMargin,2)))
                    self.total_p_value.config(text = "C$ "+str(round(self.total_positon_value,2)))
                    if self.message.cget('text') == "No Connection":
                        self.message.config(text = "connected")
            else:
                self.message.config(text = "No Connection")
            time.sleep(0.5)
    def start_stop_toggle(self,on):
        if self.trading == on:
            return
        if on == True:
            self.btn_trade_stop.grid(row = 0, column = 0, sticky = "nsew", padx = 10, pady = 10)
            self.btn_trade_start.grid_forget()
            self.trading = on
            self.session_start_time = datetime.now()
            t3 = threading.Thread(target = self.clock_update)
            t3.daemon = True
            t3.start()
        if on == False:
            self.btn_trade_start.grid(row = 0, column = 0, sticky = "nsew", padx = 10, pady = 10)
            self.btn_trade_stop.grid_forget()
            self.trading = on
            self.message.config(text = "Auto Trade")
    
    def clock_update(self):
        while self.root.winfo_exists() == True:
            try:
                time.sleep(0.1)
                if self.trading == False:
                    return
                elif self.canvas.winfo_viewable() == True and self.message.cget('text') != "No Connection":
                    elapsed_time = datetime.now() - self.session_start_time
                    elapsed_time = str(elapsed_time)
                    self.message.config(text = "Trading Duration: "+ elapsed_time[0:len(elapsed_time)-7]) 
                    # print("still going")   
            except Exception as e:
                traceback.print_tb(e.__traceback__)
                return
    
    def OnMouseWheel(self,event):
        if event.delta < 0 and self.n_of_points < 300:
            self.n_of_points += 4
        if event.delta > 0 and self.n_of_points > 20:
            self.n_of_points -= 4
        if self.n_of_points > 300:
            self.n_of_points = 300
        if self.n_of_points < 30:
            self.n_of_points = 30

    def to_floats(self,l):
        return [float(i) for i in l]
