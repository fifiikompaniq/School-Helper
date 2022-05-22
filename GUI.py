from tkinter import *
import os

top = Tk()

def callMain():
   os.system('main.py')
   Tk.MessageBox.showinfo("Main script succesfully ran!")

button = Button(top, text ="Synchornize!", command = callMain)

button.pack()
top.mainloop()
