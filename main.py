import tkinter as tk

def color(RGB):
    return '#%02x%02x%02x' % RGB

if __name__ == "__main__":
    WIDTH = 1024
    HEIGHT = 768
    # ----------------------------------------------^ Theme----------------------------------------------------
    # -----------------------------------------------Root ini + Preload Pages + Initialize Login Page-------------------------------------------------------------------------
    root = tk.Tk()
    root.title('Forex Bot')
    initx = int(root.winfo_screenwidth()/2-WIDTH/2)
    inity = int(root.winfo_screenheight()/2-HEIGHT/2)
    root.geometry(str(WIDTH) + "x" + str(HEIGHT)+"+"+str(initx)+"+"+str(inity))
    root.resizable(HEIGHT,WIDTH)
    root.columnconfigure(0,weight = 1)
    root.rowconfigure(0,weight = 1)
    username = ""
    mainpage = ""
    # root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()