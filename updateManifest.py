import PySimpleGUI as sg
import os.path
import re # for regex
from readManifest import *

# #Test function
# ship = []
# i = 1
# while i <= 8:
#     j = 1
#     while j <= 12:
#         ship.append(Container((i,j),0,'UNUSED'))
#         j+=1
#     i+=1
#
# ship[0] = Container((1,1),130,'Bob')
# ship[1] = Container((1,2),20,'Bob2')
# ship[2] = Container((1,3),50,'Bob3')
# ship[3] = Container((1,4),20,'Bob4')

def writeManifest(manifestOrigName, ship):
    save_path = "/Users/nathan/Desktop"
    completeName = os.path.join(save_path, manifestOrigName+"_OUTBOUND.txt") #https://www.adamsmith.haus/python/answers/how-to-write-a-file-to-a-specific-directory-in-python
    file = open(completeName, 'w')
    for container in ship:
        line = "[" + "{:02d}".format(container.location[0]) + "," + "{:02d}".format(container.location[1]) + "], {" + "{:05d}".format(container.weight) + "}, " + container.name + "\n"
        #https://stackoverflow.com/questions/134934/display-number-with-leading-zeros
        file.write(line)
    file.close()

# #Test function
# writeManifest("Example_manifest", ship)
