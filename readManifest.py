# import PySimpleGUI as sg
import os.path
from tkinter import *
from tkinter import filedialog
import re # for regex
from typing import NamedTuple

class Container():
    def __init__(self, location = (-1, -1), weight = 0, name = ''):
        self.location = location
        self.weight = weight
        self.name = name
    def printContainer(self):
        return self.weight


def openFile():
    global file
    filepath = filedialog.askopenfilename(initialdir="./", title="Select manifest file.")
    file = open(filepath, 'r') #'r' reads text
    ship = readFile(file)
    file.close()
    return ship
    
def getFileName():
    return os.path.basename(file.name)

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
        x_location = int(location.group(1))
        y_location = int(location.group(2))
        weight = int(location.group(3))
        name = location.group(4)
        currContainer = Container((x_location, y_location), weight, name)
        Containers.append(currContainer)
    return Containers

