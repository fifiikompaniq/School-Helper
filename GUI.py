from tkinter import *
import os

top = Tk()

def callMain():
   os.system('main.py')

button = Button(top, text ="Synchornize!", command = callMain)

button.pack()
top.mainloop()
