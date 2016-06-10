import Tkinter
import tkMessageBox
import cheeta

top = Tkinter.Tk()


def helloCallBack():
   tkMessageBox.showinfo( "Hello Python", "Hello World")

B = Tkinter.Button(top, text ="Hello", command = helloCallBack)

B.pack()

top.mainloop()
