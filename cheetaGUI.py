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

from Tkinter import *
import Tkinter as tk
from tkFileDialog   import askopenfilename
fields = 'fileName','dVal','tVal' 'lVal','popSize','numGen','verbose','limit'

class MainWindow(tk.Frame):
    counter = 0
    
    def __init__(self, *args, **kwargs):
        
        tk.Frame.__init__(self, *args, **kwargs)
        self.button = tk.Button(self, text="Create new window", 
                                command=self.createWindow)
        self.button.pack(side="top")

    def createWindow(self):
        self.counter += 1
        t = tk.Toplevel(self)
        t.wm_title("Window #%s" % self.counter)
        l = tk.Label(t, text="This is window #%s" % self.counter)
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)
    
    def initialize(self):
        pass
        
class Application(tk.Frame):
    def __init__(self, root=None):
        tk.Frame.__init__(self, root)
        self.pack()
        self.createWidgets()
        
    def createWidgets(self):
        self.QUIT = tk.Button(self, text="Quit", fg="red", command=root.destroy)
        self.QUIT.pack(side="bottom")

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
        fileMenu.add_command(label="Open file", command=OpenFile)
        fileMenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=fileMenu)
        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)

    def onExit(self):
        self.quit()

def fetch(entries):
   for entry in entries:
      field = entry[0]
      text  = entry[1].get()
      print('%s: "%s"' % (field, text)) 

def makeform(root, fields):
   entries = []
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=15, text=field, anchor='w')
      ent = Entry(row)
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries.append((field, ent))
   return entries


if __name__ == "__main__":
    def OpenFile():
        name = askopenfilename()
        print name
    root = tk.Tk()
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
    b1 = Button(root, text='Show', command=(lambda e=ents: fetch(e)))
    b1.pack(side=LEFT, padx=5, pady=5)
    menu = Menu(root)
    main = MainWindow(root)
  #  main.title("Cheeta")
    main.pack(side="top", fill="both", expand=True)
    main = Application(root)
    root.geometry('1000x900+300+300')
    app = makeMenu(root)
    root.mainloop()
