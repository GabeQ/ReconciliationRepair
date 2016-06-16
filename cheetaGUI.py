# cheetaGUI.py
#
# Created by Matt Dohlen, Chen Pekker, Gabriel Quiroz
# June 2016
#
#
#
#

from Tkinter import *

import Tkinter as tk
from tkFileDialog   import askopenfilename
from cheetaForGUI import *
import tkFont
from PIL import ImageTk, Image


fileOpened = False
fileName = None
dVal = 2
tVal = 3
lVal = 1
popSize = 30
numGen = 30
verbose = False
limit = None

fields = 'dVal','tVal','lVal','popSize','numGen','verbose','limit'

class MainWindow(tk.Frame):
    def initialize(self):
        pass
        
class Application(tk.Frame):
    def __init__(self, root=None):
        tk.Frame.__init__(self, root)
        self.pack()
        
class makeMenu(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
        self.parent.title("Cheeta")
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
   answers = []
   for entry in entries:
      if str(entry) != "verbose":
        field = entry[0]
        text  = entry[1].get()
        print ('%s: "%s"' % (field, text))
        answers.append((field, text))
      else:
          print "hi !!!"
   print "IN fetch!!"
   print answers
   return answers
   
def verboseSel():
    global verbose
    selection = var.get()
    if selection == 1:
        verbose = True
    else:
        verbose = False
    return verbose

def makeForm(root, fields):
   global dVal, tVal, lVal, popSize, numGen, verbose, limit
   entries = []
   for field in fields:
       
      # naming the labels
      labelText=StringVar()
      if str(field) == "dVal":
          labelText.set("D(uplicate)")
      elif str(field) == "tVal":
          labelText.set("T(ransfer)")
      elif str(field) == "lVal":
          labelText.set("L(oss)")
      elif str(field) == "popSize":
          labelText.set("Population size")
      elif str(field) == "numGen":
          labelText.set("Number of generations")
      elif str(field) == "verbose":
          labelText.set("Verbose")
      else:
          labelText.set("Limit")
      labelE=Label(root, textvariable=labelText)
      labelE.pack(side="top")
      
      # creating the inputs
      if str(field) == "verbose":
          verbOn = Radiobutton(root, text="On", padx = 15, variable=var, value=1, command=verboseSel)
          verbOn.pack(side="top")
          verbOff = Radiobutton(root, text="Off", padx = 15, variable=var, value=2, command=verboseSel)
          verbOff.pack(side="top")          
          
      else:
          textHere=Entry(root,textvariable=("default"),width=120)
          textHere.pack(side="top")
      inputGiven = Entry(textHere)
      inputGiven.pack(side="top")
      if str(field) != "verbose":
           entries.append((field, inputGiven))
      
   print "makeForm HIHI", entries
   return entries
   
def retrieveInput(inputs):
    entries = fetch(inputs)
    print "IN retrieveInput"
    print "entries: ", entries
    global fileName, fileOpened, dVal, tVal, lVal, popSize, numGen, verbose, limit
    for i in entries:
        if i[0] == 'fileName' and fileOpened == False:
            fileName = i[1]
        elif i[0] == 'dVal':
            if i[1] != "":
                dVal = i[1]
        elif i[0] == 'tVal':
            if i[1] != "":
                tVal = i[1]
        elif i[0] == 'lVal':
            if i[1] != "":
                lVal = i[1]
        elif i[0] == 'popSize':
            if i[1] != "":
                popSize = i[1]
        elif i[0] == 'numGen':
            if i[1] != "":
                numGen = i[1]
        elif i[0] == 'limit':
            if i[1] != "":
                limit = i[1]
    return fileName, dVal, tVal, lVal, popSize, numGen, verbose, limit
   
def callCheeta():
 #   runningCheetaText()
    global verbose
    fileName, dVal, tVal, lVal, popSize, numGen, verbose, limit = retrieveInput(inputs)
    print "NEEDED: ", fileName, dVal, tVal, lVal, popSize, numGen, verbose, limit
    answer = cheeta(fileName, dVal, tVal, lVal, popSize, numGen, verbose, limit)
    displayAnswer(answer)

def displayAnswer(answer):
    outputMessage.delete(1.0, END)    
    outputMessage.pack()
    outputMessage.insert(END, answer)
    
"""
def showButton():
    outputMessage.delete(1.0, END)    
    outputMessage.pack()
    answer = makeForm(root, fields)
    outputMessage.insert(END, answer)"""
    
def OpenFile():
    global fileOpened, fileName
    fileOpened = True
    uploadedName = askopenfilename()
    fileName = uploadedName
    name = "Uploaded file: " + uploadedName
    displayAnswer(name)
    return fileOpened, fileName

if __name__ == "__main__":
    root = tk.Tk()
    # upload an image for background
    im = Image.open('jungle2.jpg')
    tkimage = ImageTk.PhotoImage(im)
    myvar=tk.Label(root,image = tkimage)
    myvar.place(x=0, y=0, relwidth=1, relheight=1)
    
    var = IntVar()
    outputMessage = Text(root, height=50, width=100, relief='flat', bg='orange2')
    
    inputs = makeForm(root, fields)
    print "INPUTS FROM MAKEFORM: ", inputs
    fileNum, dVal, tVal, lVal, popSize, numGen, verbose, limit = retrieveInput(inputs)
    root.bind('<Return>', (lambda event, e=inputs: fetch(e)))   
 
    # create button 
    b = Button(root, text="Run Cheeta", command=callCheeta)
    b.pack()
    
    menu = Menu(root)
    app = makeMenu(root)
    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True)
    main = Application(root)
    
    # display initial message
    default = "The default and current settings are: \n" \
    "fileName = None \n" \
    "Duplication cost = 2 \n" \
    "Tranfer cost = 3 \n" \
    "Loss cost = 1 \n" \
    "Population size = 30 \n" \
    "Number of generations = 30 \n" \
    "Verbose = False \n" \
    "Limit = None \n"
    displayAnswer(default)
    
    
    
    root.geometry('1000x900+300+300')
  #  root.configure(bg='orange2')
    root.mainloop()
