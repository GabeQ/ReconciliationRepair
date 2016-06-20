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
from cheeta import *
import tkFont
from PIL import ImageTk, Image
from CheetaExceptions import CheetaError, CheetaErrorEnum



fileOpened = False
fileName = None
dVal = 2
tVal = 3
lVal = 1
popSize = 30
numGen = 30
verbose = False
limit = None
cheetaLog = ""

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
   print "IN fetch!!", answers
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
   count = 0
   for field in fields:
      count = count + 20
      # naming the labels
      labelText = StringVar()
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
      labelE=Label(root,bg='orange2', borderwidth=.00001, textvariable=labelText)
      labelE.pack(side="top")
    #  labelE.grid(row=1, column=(0 + count))
      
      # creating the inputs
      if str(field) == "verbose":
          verbOn = Radiobutton(root,borderwidth=.00001, bg='orange2', text="On", padx = 15, variable=var, value=1, command=verboseSel)
          verbOn.pack(side="top")
          verbOff = Radiobutton(root,borderwidth=.00001, bg='orange2', text="Off", padx = 15, variable=var, value=2, command=verboseSel)
          verbOff.pack(side="top")      
      else:
        #  count = count + 20
          textHere=Entry(root, borderwidth=.00001, bg='orange2',textvariable=("default"),width=25)
          textHere.pack(side="top")
        #  textHere.grid(row=1, column=(0 + count))
          inputGiven = Entry(textHere)
          inputGiven.pack(side="top")
          entries.append((field, inputGiven))
      
   print "in makeForm HI HI", entries
   return entries
   
def retrieveInput(inputs):
    entries = fetch(inputs)
    print "IN retrieveInput"
    print "entries: ", entries
    global fileName, fileOpened, dVal, tVal, lVal, popSize, numGen, verbose, limit
    for i in entries:
        if i[0] == 'dVal':
            if i[1] != "":
                dVal = int(i[1])
        elif i[0] == 'tVal':
            if i[1] != "":
                tVal = int(i[1])
        elif i[0] == 'lVal':
            if i[1] != "":
                lVal = int(i[1])
        elif i[0] == 'popSize':
            if i[1] != "":
                popSize = int(i[1])
        elif i[0] == 'numGen':
            if i[1] != "":
                numGen = int(i[1])
        elif i[0] == 'limit':
            if i[1] != "":
                limit = int(i[1])
    return fileName, dVal, tVal, lVal, popSize, numGen, verbose, limit
   
def callCheeta():
    global verbose, cheetaLog  
    fileName, dVal, tVal, lVal, popSize, numGen, verbose, limit = retrieveInput(inputs)
    if fileName == None:
        print "Please upload a file in either '.tree' or '.newick' format. To upload click 'File' then 'Open file.'"
        cheetaLog = "Please upload a file in either '.tree' or '.newick' format. To upload click 'File' then 'Open file.'"
    else:
        cheetaLog = "Cheeta parameters:  \n" \
        "fileName = " + fileName + " \n" \
        "Duplication cost = " + str(dVal) + " \n" \
        "Tranfer cost = " + str(tVal) + " \n" \
        "Loss cost = " + str(lVal) + " \n" \
        "Population size = " + str(popSize) + " \n" \
        "Number of generations = " + str(numGen) + " \n" \
        "Verbose = " + str(verbose) + " \n" \
        "Limit = " + str(limit) + " \n" \
        " \n" 
        
        print "NEEDED: ", fileName, dVal, tVal, lVal, popSize, numGen, verbose, limit     
        try:
            fixerCost, fixerLog, DPCost, janeCost = cheeta(fileName, dVal, tVal, lVal, popSize, numGen, verbose, limit)
        except CheetaError as e:
            print str(e)
            raise
        except:
            print "Unknown error has occurred. Check Error Log"
            raise
        
        # check Verbose
        if verbose == True:
            cheetaLog = cheetaLog + fixerLog + "\r\n"
            
        # compare fixer score with Jane score
        if DPCost == janeCost:  # Jane's solution is optimal
            print "Jane Solution Cost: " + str(janeCost)
            print "Theoretical Lower Bound: " + str(DPCost)
            print "Jane's Solution is Optimal"
            cheetaLog = cheetaLog + "Jane Solution Cost: " + str(janeCost) + " \n" + "Theoretical Lower Bound: " + str(DPCost) + " \n" + "Jane's Solution is Optimal"
    
        elif fixerCost < janeCost:  # fixer found a better solution than Jane
            print "Jane Solution Cost: " + str(janeCost)
            print "Theoretical Lower Bound: " + str(DPCost)
            print "Cheeta found a valid solution of cost: " + str(fixerCost)
            print "You may wish to try running Jane again with larger values for the population and/or generation parameters"
            cheetaLog = cheetaLog + "Jane Solution Cost: " + str(janeCost) + " \n" + "Theoretical Lower Bound: " + str(DPCost) + " \n" + "You may wish to try running Jane again with larger values for the population and/or generation parameters"
    
        else:  # fixer was unable to find a better solution than Jane
            print "Jane Solution Cost: " + str(janeCost)
            print "Theoretical Lower Bound: " + str(DPCost)
            print "Cheeta was unable to find a valid solution better than Jane"
            print "You may wish to try running Jane again with larger values for the population and/or generation parameters"
            cheetaLog = cheetaLog + "Jane Solution Cost: " + str(janeCost) + " \n" + "Theoretical Lower Bound: " + str(DPCost) + " \n" + "Cheeta was unable to find a valid solution better than Jane" + " \n" + "You may wish to try running Jane again with larger values for the population and/or generation parameters"
        
    displayAnswer(cheetaLog)

def displayAnswer(answer):
    outputMessage.delete(1.0, END)    
    outputMessage.pack(side='bottom')
    outputMessage.insert(END, answer)
    
def OpenFile():
    global fileOpened, fileName
    fileOpened = True
    uploadedName = askopenfilename(filetypes=[('Newick files', '*.newick'),('Tree files', '*.tree'),('Nwk files', '*.nwk')])
    fileName = uploadedName
    name = "Uploaded file: " + uploadedName
    displayAnswer(name)
    return fileOpened, fileName

def make_label(parent, img):
    label = Label(parent, image=img)
    label.pack()


if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap(r'cooltext.png')
    
    # upload an image for background
    im = Image.open('wowmonkey.jpg')
    tkimage = ImageTk.PhotoImage(im)
    myvar=tk.Label(root,image = tkimage)
    myvar.place(x=0, y=0, relwidth=1, relheight=1)
    
    # create variables
    var = IntVar()
    outputMessage = Text(root, height=51, width=100, relief='flat', bg='orange2', font =(15)) 
    
    inputs = makeForm(root, fields)
    print "INPUTS FROM MAKEFORM: ", inputs  
 
    # create button 
    b = Button(root,borderwidth=.00001, text="Run Cheeta", command=callCheeta)
    b.pack()
    
    menu = Menu(root)
    app = makeMenu(root)
    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True)
    main = Application(root)
    root.geometry('1000x900+300+300')
    
    # display initial message
    default = "Welcome to Cheeta! \n" \
    " \n" \
    "The default and current settings are: \n" \
    "fileName = None \n" \
    "Duplication cost = 2 \n" \
    "Tranfer cost = 3 \n" \
    "Loss cost = 1 \n" \
    "Population size = 30 \n" \
    "Number of generations = 30 \n" \
    "Verbose = Off \n" \
    "Limit = None \n"
    displayAnswer(default)
    
  #  root.configure(bg='orange2')
    root.mainloop()
