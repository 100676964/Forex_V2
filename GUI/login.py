from tkinter import *
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from User_Data import authendication as auth

class login_gui:
    def __init__(self,root:Tk,theme:dict) -> None:
        for child in root.winfo_children():
            child.destroy()
        canvas = Canvas(root,background='grey')
        
        canvas.rowconfigure(0,weight = 1)
        canvas.rowconfigure(1,weight = 2)
        canvas.rowconfigure(2,weight = 1)
        canvas.columnconfigure(0,weight = 1)
        canvas.columnconfigure(1,weight = 2)
        canvas.columnconfigure(2,weight = 1)
        canvas.grid(row=0,column=0,sticky='nsew')

        self.inner_canvas = Canvas(canvas,background= theme.get('background_color'),highlightbackground = theme.get('widgetBgColor'))
        self.inner_canvas.grid(row = 1,column = 1,sticky = 'nsew')

        self.inner_canvas.rowconfigure(0,weight = 2)
        self.inner_canvas.rowconfigure(1,weight = 0)
        self.inner_canvas.rowconfigure(2,weight = 0)
        self.inner_canvas.rowconfigure(3,weight = 0)
        self.inner_canvas.rowconfigure(4,weight = 0)
        self.inner_canvas.rowconfigure(5,weight = 0)
        self.inner_canvas.rowconfigure(6,weight = 2)

        self.inner_canvas.columnconfigure(0,weight = 1)
        self.inner_canvas.columnconfigure(1,weight = 0)
        self.inner_canvas.columnconfigure(2,weight = 0)
        self.inner_canvas.columnconfigure(3,weight = 1)

        # ------------------------------------------------------Welcome Message------------------------------------------------------------
        self.message = Label(self.inner_canvas, text='Welcome', font=theme.get('labelFonts'), background=theme.get('widgetBgColor'))
        self.message.grid(row = 1, column = 1, columnspan=2,sticky = "ew")

        # ------------------------------------------------------User Input Area-------------------------------------------------------------
        
        Label(self.inner_canvas, text='User Name', font = theme.get('labelFonts'), background = theme.get('widgetBgColor')).grid(row = 2, column = 1,sticky = "nswe",padx= (0,10),pady=10)
        self.name_entry = Entry(self.inner_canvas,font = "Calibri 15")
        self.name_entry.grid(row = 2, column = 2,sticky = "nsw",padx = (10,0),pady=10)
        
        
        Label(self.inner_canvas, text='Password', font = theme.get('labelFonts'), background = theme.get('widgetBgColor')).grid(row = 3, column = 1,sticky = "nswe",padx=(0,10),pady=10)
        self.password_entry = Entry(self.inner_canvas,font = "Calibri 15", show = "$")
        self.password_entry.grid(row = 3, column = 2,sticky = "nsw",padx = (10,0),pady=10)

        # ------------------------------------------------------Login Button---------------------------------------------------------------
        Button(self.inner_canvas, text = 'Log In', font = theme.get('buttonFonts'), background = theme.get('widgetBgColor'), activebackground = theme.get('pressedColor'),command=self.authendicate ).grid(row = 4, column = 1,columnspan=2,sticky = "ew")
        Button(self.inner_canvas, text = 'Create New User', font = theme.get('buttonFonts'), background = theme.get('widgetBgColor'),activebackground = theme.get('pressedColor'),).grid(row = 5, column = 1,columnspan=2,sticky = "ew",pady = (10,0))
    
    def authendicate(self):
        if len(self.name_entry.get()) != 0 and len(self.password_entry.get()) != 0:
            auth_result = auth.check_user(self.name_entry.get(),self.password_entry.get())
            if auth_result[0] == True:
                pass
                # self.accessfunction(self.name_entry.get(),auth_result[1],auth_result[2])
            else:
                self.message.config(text = "Access Denied!")
        else:
            self.message.config(text = "Enter Fields!")