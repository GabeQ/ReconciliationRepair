#from Tkinter import *
#import tkMessageBox
#class MainWindow(tk.Frame):
##sets the base screen for the GUI
#base = Tk()
#
##sets the Menu Bar for the GUI
#menubar = Menu(base)
#filemenu = Menu(menubar, tearoff = 0) #File
#filemenu.add_command(label = "Open File")
#filemenu.add_separator()
#filemenu.add_command(label = "Exit", command = base.quit)
#menubar.add_cascade(label = "File", menu = filemenu)
#
#settingmenu = Menu(menubar, tearoff = 0) #Settings
#settingmenu.add_command(label = "Set Costs", )
#menubar.add_cascade(label = "Settings", menu = settingmenu)
#
#
#
#
#base.config(menu = menubar)
#base.mainloop()

import Tkinter as tk

class MainWindow(tk.Frame):
    counter = 0
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.button = tk.Button(self, text="Create new window", 
                                command=self.create_window)
        self.button.pack(side="top")

    def create_window(self):
        self.counter += 1
        t = tk.Toplevel(self)
        t.wm_title("Window #%s" % self.counter)
        l = tk.Label(t, text="This is window #%s" % self.counter)
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)

if __name__ == "__main__":
    root = tk.Tk()
    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()
