# hello_world.py

import PySimpleGUI as sg
import os.path
from tkinter import *
from tkinter import filedialog
#from tkinter filedialog

def openFile():
    filepath = filedialog.askopenfilename(initialdir="/Users/lizbethareizaga/Documents/CS179/CS179M",
                                            title="Select manifest file.")
    file = open(filepath, 'r') #r'r' reads text
    print(file.read())
    file.close()

window = Tk()
button = Button(text="Open", command=openFile)
button.pack()
window.mainloop()
