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

from Tkinter import Tk, Frame, Menu
import Tkinter as tk
#import tkMessageBox

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
        
class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.QUIT = tk.Button(self, text="Quit", fg="red",
                              command=root.destroy)
        self.QUIT.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")
        
class makeMenu(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
        
        
    def initUI(self):
      
        self.parent.title("Simple menu")
        
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Upload file", command=self.onExit)
        fileMenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=fileMenu)
        

    def onExit(self):
        self.quit()
    

if __name__ == "__main__":
    root = tk.Tk()
    main = MainWindow(root)
 #   main.title("Cheeta")
    main.pack(side="top", fill="both", expand=True)
    main = Application(master=root)
    root.geometry('800x600+300+300')
    app = makeMenu(root)
    root.mainloop()
