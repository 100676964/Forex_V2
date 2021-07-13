from tkinter import *
import traceback 
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from User_Data import authendication as auth
class registration:
    def __init__(self,root:Tk,theme:dict,switch) -> None:
            self.switch = switch
            self.canvas = Canvas(root,background=theme.get('background_color'))
            self.canvas.rowconfigure(0,weight = 1)
            self.canvas.rowconfigure(1,weight = 2)
            self.canvas.rowconfigure(2,weight = 1)
            self.canvas.columnconfigure(0,weight = 1)
            self.canvas.columnconfigure(1,weight = 2)
            self.canvas.columnconfigure(2,weight = 1)
            
            

            self.inner_canvas = Canvas(self.canvas,background= 'grey',highlightbackground = theme.get('widgetBgColor'))
            self.inner_canvas.grid(row = 1,column = 1,sticky = 'nsew')

            self.inner_canvas.rowconfigure(0,weight = 1)
            self.inner_canvas.rowconfigure(1,weight = 0)
            self.inner_canvas.rowconfigure(2,weight = 0)
            self.inner_canvas.rowconfigure(3,weight = 0)
            self.inner_canvas.rowconfigure(4,weight = 0)
            self.inner_canvas.rowconfigure(5,weight = 0)
            self.inner_canvas.rowconfigure(6,weight = 0)
            self.inner_canvas.rowconfigure(7,weight = 0)
            self.inner_canvas.rowconfigure(8,weight = 2)

            self.inner_canvas.columnconfigure(0,weight = 1)
            self.inner_canvas.columnconfigure(1,weight = 0)
            self.inner_canvas.columnconfigure(2,weight = 0)
            self.inner_canvas.columnconfigure(3,weight = 1)

            #.......................................Message....................................................
            self.message = Label(self.inner_canvas,text = "Registration", background = theme.get('widgetBgColor'), font = theme.get('labelFonts') , foreground= theme.get('widgetBgColor'))
            self.message.grid(row = 1, column = 1, columnspan = 2, sticky = 'ew')

            Label(self.inner_canvas, text='User Name:', font = theme.get('labelFonts'), background = theme.get('widgetBgColor')).grid(row = 2, column = 1,sticky = "nswe",padx= (0,10),pady=10)
            self.name_entry = Entry(self.inner_canvas,font = "Calibri 15")
            self.name_entry.grid(row = 2, column = 2,sticky = "nsw",padx = (10,0),pady=10)

            #......................................Rgistration Form.............................................        
            Label(self.inner_canvas, text='Password:', font = theme.get('labelFonts'), background = theme.get('widgetBgColor')).grid(row = 3, column = 1,sticky = "nswe",padx=(0,10),pady=10)
            self.password_entry = Entry(self.inner_canvas,font = "Calibri 15")
            self.password_entry.grid(row = 3, column = 2,sticky = "nsw",padx = (10,0),pady=10)

            Label(self.inner_canvas, text='Confirm Password:', font = theme.get('labelFonts'), background = theme.get('widgetBgColor')).grid(row = 4, column = 1,sticky = "nswe",padx=(0,10),pady=10)
            self.password_confirm = Entry(self.inner_canvas,font = "Calibri 15")
            self.password_confirm.grid(row = 4, column = 2,sticky = "nsw",padx = (10,0),pady=10)

            Label(self.inner_canvas, text='Oanda AccountID:', font = theme.get('labelFonts'), background = theme.get('widgetBgColor')).grid(row = 5, column = 1,sticky = "nswe",padx=(0,10),pady=10)
            self.ID = Entry(self.inner_canvas,font = "Calibri 15")
            self.ID.grid(row = 5, column = 2,sticky = "nsw",padx = (10,0),pady=10)

            Label(self.inner_canvas, text='Access Token:', font = theme.get('labelFonts'), background = theme.get('widgetBgColor')).grid(row = 6, column = 1,sticky = "nswe",padx=(0,10),pady=10)
            self.token_entry = Entry(self.inner_canvas,font = "Calibri 15")
            self.token_entry.grid(row = 6, column = 2,sticky = "nsw",padx = (10,0),pady=10)

            #......................................Button.............................................  
            Button(self.inner_canvas, text = 'Submit', font = theme.get('buttonFonts'), background = theme.get('widgetBgColor'), activebackground = theme.get('pressedColor'), command = self.register).grid(row = 7, column = 1,sticky = "ew", padx = 5)
            Button(self.inner_canvas, text = 'Cancel', font = theme.get('buttonFonts'), background = theme.get('widgetBgColor'), activebackground = theme.get('pressedColor'), command = self.cancel).grid(row = 7, column = 2,sticky = "ew", padx = 5)

        

    def register(self):
        if len(self.name_entry.get()) == 0:
                self.message.config(text = "Please Enter A Name!")

        elif len(self.password_entry.get()) == 0:
                self.message.config(text = "Please Enter A Password!")

        elif self.password_confirm.get() != self.password_entry.get():
                self.message.config(text = "Please Verify Your Password")

        elif len(self.ID.get()) == 0:
                self.message.config(text = "Please Enter Your Oanda Trading Password")

        elif len(self.token_entry.get()) == 0:
                self.message.config(text = "Please Enter Your Oanda API Token")
        else:
            from API import oanda
            call = oanda.OandaAPI(self.ID.get(),self.token_entry.get())
            try:
                    if call.get_acct_info() is not None:
                            flag = auth.create_new_user(self.name_entry.get(),self.password_entry.get(),self.ID.get(),self.token_entry.get())
                            if flag == 0:
                                    self.message.config(text = "You Have Registerd!")

                            elif flag == 1:
                                    self.message.config(text = "Registration Failed!")
                                    
                            elif flag == 2:          
                                    self.canvas.grid_forget()
                    else:
                            self.message.config(text = "Useless Token")
            except Exception as e:
                    
                    traceback.print_tb(e.__traceback__)

    def cancel(self):
        self.switch.go_to_login()