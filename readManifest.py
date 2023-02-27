import PySimpleGUI as sg
import os.path
from tkinter import *
from tkinter import filedialog
import re # for regex
from typing import NamedTuple

class Container(NamedTuple):
    location: tuple
    weight: int
    name: str


def openFile():
    filepath = filedialog.askopenfilename(initialdir="/Users/lizbethareizaga/Documents/CS179/CS179M",
                                            title="Select manifest file.")
    file = open(filepath, 'r') #'r' reads text
    print(readFile(file))
    file.close()

'''readFile(file)
        Inputs: text file -- manifest that contains information about containers on ships
        Output: list of containers on the ship
'''
def readFile(file):
    containers = file.readlines()
    currLine = 0
    Containers = []
    for line in containers:
        ++currLine
        #for every line get the location ex: [01,01], {weight}, Container name
        #location_x = #use regex to find x location
        #location_y = #use regex to find y location
        #weight = #use regex to find weight
        #name = #use regex to find name
        location = re.search("\[(\d\d),(\d\d)\], \{(\d{5})\}, ([^\n]*)", line) #figure out container name specs
        x_location = location.group(1)
        y_location = location.group(2)
        weight = location.group(3)
        name = location.group(4)
        currContainer = Container((x_location, y_location), weight, name)
        Containers.append(currContainer)
    return Containers

window = Tk()
window.geometry("700x900")
button = Button(text="Open", command=openFile)
button.pack()
window.mainloop()
