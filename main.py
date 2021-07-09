from tkinter import *
from GUI import login
def color(RGB):
    return '#%02x%02x%02x' % RGB

if __name__ == "__main__":
    WIDTH = 1024
    HEIGHT = 768

    # all widgets background color
    theme = {
                'widgetBgColor' : color((200, 150, 10)),
                'pressedColor' : color((230, 180, 10)),
                'widgetFgColor' : color((10, 10, 10)),
                'background_color' : color((8, 8, 10)),
                'labelFonts' : ('Arial',15, 'bold'),
                'buttonFonts' : ('Arial', 12, 'bold')
            }

    # button pressed color
    

    # font color

    # canvas background color



    # ----------------------------------------------^ Theme----------------------------------------------------
    # -----------------------------------------------Root ini + Preload Pages + Initialize Login Page-------------------------------------------------------------------------
    root = Tk()
    root.title('Forex Bot')
    initx = int(root.winfo_screenwidth()/2-WIDTH/2)
    inity = int(root.winfo_screenheight()/2-HEIGHT/2)
    root.geometry(str(WIDTH) + "x" + str(HEIGHT)+"+"+str(initx)+"+"+str(inity))
    root.resizable(HEIGHT,WIDTH)
    root.columnconfigure(0,weight = 1)

    root.rowconfigure(0,weight = 1)

    username = ""
    mainpage = ""
    login.login_gui(root,theme)
    # root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()