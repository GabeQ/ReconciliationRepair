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
      field = entry[0]
      text  = entry[1].get()
      print ('%s: "%s"' % (field, text))
      answers.append((field, text)) 
   return answers

def makeForm(root, fields):
   global dVal, tVal, lVal, popSize, numGen, verbose, limit
   entries = []
   for field in fields:
      labelText=StringVar()
      labelText.set(str(field))
      print "labelText", labelText
      labelE=Label(root, textvariable=labelText)
      labelE.pack(side="top")
      print "labelE", labelE
      title=StringVar(None)
      textHere=Entry(root,textvariable=title,width=500)
      textHere.pack(side="top")
      textHere.insert(0, str(field))
      #lab = Label(textHere, width=15, text=field, anchor='w')
      inputGiven = Entry(textHere)
      
      #lab.pack(side=LEFT)
      inputGiven.pack(side=RIGHT, expand=YES, fill=X)
      
      entries.append((field, inputGiven))
   print "In makeForm"
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
        elif i[0] == 'verbose':
            if i[1] != "":
                verbose = i[1]
        elif i[0] == 'limit':
            if i[1] != "":
                limit = i[1]
    return fileName, dVal, tVal, lVal, popSize, numGen, verbose, limit
   
def callCheeta():
 #   runningCheetaText()
    fileName, dVal, tVal, lVal, popSize, numGen, verbose, limit = retrieveInput(inputs)
    answer = cheeta(fileName, dVal, tVal, lVal, popSize, numGen, verbose, limit)
    displayAnswer(answer)
    
"""
def runningCheetaText():
    outputMessage.delete(1.0, END)    
    outputMessage.pack()
    outputMessage.insert(END, "running Cheeta... This may take a few minutes.")
    """

def displayInputFile(answer):
    inputFile.delete(1.0, END)    
    inputFile.pack()
    inputFile.insert(END, "Uploaded file: " + answer)

def displayAnswer(answer):
    outputMessage.delete(1.0, END)    
    outputMessage.pack()
    outputMessage.insert(END, answer)
    
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
    outputMessage = Text(root, height=50, width=100)
    inputs = makeForm(root, fields)
    print "INPUTS FROM MAKEFORM: ", inputs
    fileNum, dVal, tVal, lVal, popSize, numGen, verbose, limit = retrieveInput(inputs)
    root.bind('<Return>', (lambda event, e=inputs: fetch(e)))   
    b1 = Button(root, text='Show', command=(lambda e=inputs: fetch(e)))
    b1.pack(side=LEFT, padx=5, pady=5)
    b = Button(root, text="Run Cheeta", command=callCheeta)
    b.pack()
    menu = Menu(root)
    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True)
    main = Application(root)
    root.geometry('1000x900+300+300')
    app = makeMenu(root)
    root.mainloop()
