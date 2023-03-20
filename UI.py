# import PySimpleGUI as psg
# names = ["Bob","Bob2"]
# lst = psg.Listbox(names, size=(20, 4), font=('Arial Bold', 14), expand_y=True, enable_events=True, key='-LIST-',select_mode="multiple")
# layout = [
#    [lst],
#    [psg.Text("", key='-MSG-', font=('Arial Bold', 14), justification='center')],
#    [psg.Button('Exit')],
# ]
# window = psg.Window('Listbox Example', layout, size=(600, 200))
# while True:
#    event, values = window.read()
#    if event in (psg.WIN_CLOSED, 'Exit'):
#       print(values['-LIST-'])
# window.close()


import time
import datetime as dt
from readManifest import *
from algorithm import *
import PySimpleGUI as sg

manifest_ship = []

logfile = "Logfile_2022.txt" #temp var-- change to ask file name when program starts

def writeToLog (fileName, comment):
    date = dt.datetime.now()
    file = open(fileName, 'a')
    file.write(date.strftime('%B %d, %Y') + ": " + time.strftime('%H:%M:%S') + ' ' )
    file.write(comment)
    file.write('\n')
    file.close()


def main_page(name, fileName):
    sg.theme('LightGray1')  #Can change theme https://www.geeksforgeeks.org/themes-in-pysimplegui/
    font = ('Arial', 30)

    names = name #Name of the employee logging in, passed in as argument of function

    layout = [
        [sg.Text(fileName,font = font,),sg.Text('',font = font,pad = (200,0),key = 'time'),sg.Text(names,font = font,pad = ((20,0),(0,0)))],
        #File name on top left, Time in the center, and employee name at the right
        #Employee Name is blank before anyone logs in
        [sg.Text('',size = (0,15))],
        #Empty Line for Spacing
        [sg.Button('Load/Unload',size=(10,2),pad = ((50,0),(0,0)),font = font), sg.Button('Balance',pad = ((125,0),(0,0)),size=(10,2),font = font)],
         ##NOTE If ship name is long the title gets messed up

        #Loading and Unloading button the left, Balancing button on the right
        [sg.Text('',size = (0,15))],
        [sg.Button('Comments',size=(10,2),font = ('Arial',14)), sg.Button('Upload',pad = (200,0),size = (10,2),font = ('Arial',14)),sg.Button('Login',size=(10,2),font = ('Arial',14))]
        #Comments button on the bottom left, Log in button on the bottom right
    ]

    window = sg.Window('Main Page', layout, size=(900, 700),finalize = True)

    while True:
        event, values = window.read(timeout=10) #Timeout is required for updating clock
        if event == 'Login': #Employee clicks Login button
            window.close()
            signin_page(name,fileName,'main','','','')
        elif event == 'Comments': #Employee clicks Comments button
            window.close()
            comments_page(name, fileName, 'main','','','')
        elif event == 'Load/Unload': #Employee clicks Loading/Unloading button
            window.close()
            unloading_loading_page(name,fileName)
        elif event == 'Balance': #Employee clicks Balancing button
            window.close()
            balancing_page(name,fileName)
        elif event == 'Upload': #Employee clicks Upload to upload manifest
            window.close()
            upload_file(name)
        elif event == sg.WIN_CLOSED: #Employee clicks the X on the program
            exit()
        window['time'].update(time.strftime('%H:%M:%S')) #Update clock in real time (Military time, local time)

    window.close()

def upload_file(name):
    global manifest_ship
    manifest_ship = openFile()
    main_page(name,getFileName())


def signin_page(name, fileName, function_call,containers_to_unload,toLoad,unLoad): #function_call tells which function is calling this function
    sg.theme('LightGray1')  #Can change theme https://www.geeksforgeeks.org/themes-in-pysimplegui/
    font = ('Arial',15)

    layout = [
    [sg.Text('Sign in',font = font)],
    [sg.Text('Name', font = font), sg.InputText(size=(50,10),expand_y = True)], #Text box for signing in
    [sg.Submit(), sg.Cancel()] #Submit button and hitting enter both submits the text
    ]

    window = sg.Window('Sign In Page', layout)
    event, values = window.read()
    window.close()
    loginName = values[0] + " signs in"
    writeToLog(logfile, loginName)
    if function_call == 'main':
        main_page(values[0],fileName) #Open the main page after closing the sign in page, passing in the name typed in as argument
    elif function_call == 'load unload':
        unloading_loading_page(values[0],fileName)
    elif function_call == 'balance':
        balancing_page(values[0],fileName)
    elif function_call == 'moves':
        moves_page(values[0],fileName)
    elif function_call == 'load page':
        load_page(name,fileName,containers_to_unload)
    elif function_call == 'calculate unload':
        calculate_unload(name,fileName,toLoad,unLoad)
        


def comments_page(name, fileName,function_call,containers_to_unload,toLoad,unLoad): #function_call tells which function is calling this function
    sg.theme('LightGray1')  #Can change theme https://www.geeksforgeeks.org/themes-in-pysimplegui/
    font = ('Arial',15)

    layout = [
    [sg.Text('Enter your comment:')],
    [sg.Multiline(size=(50, 20))], #Multi-line input box, employee has to click 'Submit' to submit the comment, enter does not submit
    [sg.Button('Submit')]
    ]

    window = sg.Window('Comment Page', layout, font = font)
    event, values = window.read()
    window.close()
    comment = values[0]
    writeToLog(logfile, comment)
    if function_call == 'main':
        main_page(name, fileName)   #Open the main page after closing the comments page, passing in the name typed in as argument
    elif function_call == 'load unload':
        unloading_loading_page(name,fileName)
    elif function_call == 'balance':
        balancing_page(name,fileName)
    elif function_call == 'moves':
        moves_page(name,fileName)
    elif function_call == 'load page':
        load_page(name,fileName,containers_to_unload)
    elif function_call == 'calculate unload':
        calculate_unload(name,fileName,toLoad,unLoad)
    #TODO: Add variable to store the comments made

def unloading_loading_page(names,fileName):
    sg.theme('LightGray1')
    font = ('Arial',30)
    name = []
    initialState = Node()
    initialState.ship = manifest_ship
    for i in manifest_ship:
        if i.name != 'UNUSED' and i.name != 'NAN':
            name.append(i.name)
            
    lst = sg.Listbox(name, size=(20, 4), font=('Arial Bold', 14), expand_y=True, enable_events=True, key='-LIST-',select_mode="multiple")

    layout = [
    [sg.Text(fileName,font = font),sg.Text('',font = font,pad = (200,0),key = 'time'),sg.Text(names,font = font,pad = ((20,0),(0,0)))],
    [sg.Text('',size = (0,3))],
    [lst],
    [sg.Text('',size = (0,3))],
    [sg.Button('Comments',size=(10,2),font = ('Arial',14)), sg.Button('Done',pad = (200,0),size = (10,2),font = ('Arial',14)),sg.Button('Login',size=(10,2),font = ('Arial',14))]
    ]

    
    window = sg.Window('Loading Unloading Page', layout, size=(900, 700),finalize = True)
    while True:
        event, values = window.read(timeout = 10)
        containers_to_unload = values['-LIST-']
        if event == 'Login': #Employee clicks Login button
            window.close()
            signin_page(names, fileName, 'load unload','','','')
        elif event == 'Comments': #Employee clicks Comments button
            window.close()
            comments_page(names,fileName,'load unload','','','')
        elif event == 'Done':
            window.close()
            containers_to_unload = values['-LIST-']
            load_page(names,fileName,containers_to_unload)
        elif event == sg.WIN_CLOSED: #Employee clicks the X on the program
            exit()
        window['time'].update(time.strftime('%H:%M:%S')) #Update clock in real time (Military time, local time)

        #TODO add implementation for done button
    window.close()
    
def load_page(names,fileName,containers_to_unload):
    sg.theme('LightGray1')
    font = ('Arial',30)
    toLoad= []
    
    layout = [
    [sg.Text(fileName,font = font),sg.Text('',font = font,pad = (200,0),key = 'time'),sg.Text(names,font = font,pad = ((20,0),(0,0)))],
    [sg.Text('Enter name and weight for containers to load:',font = font)],
    [sg.Text('If there are no containers to load press "Done".',font = ('Arial',20))],
    [sg.Text('Name',size = (15,1),font = font),sg.InputText(key = 'input')],
    [sg.Text('Weight',size = (15,1),font = font),sg.InputText(key = 'input2')],
    [sg.Button('Add container',size = (10,1),font = ('Arial,14'))],
    [sg.Button('Comments',size=(10,2),font = ('Arial',14)), sg.Button('Done',pad = (200,0),size = (10,2),font = ('Arial',14)),sg.Button('Login',size=(10,2),font = ('Arial',14))]
    ]
    window = sg.Window('Balancing Page', layout, size=(900, 700),finalize = True)

    while True:
        event, values = window.read(timeout = 10)
        if event == 'Login': #Employee clicks Login button
            window.close()
            signin_page(names, fileName, 'load page',containers_to_unload,'','')
        elif event == 'Comments': #Employee clicks Comments button
            window.close()
            comments_page(names,fileName,'load page',containers_to_unload,'','')
        elif event == 'Done':
            window.close()
            calculate_unload(names,fileName,toLoad,containers_to_unload)
        elif event == 'Add container':
            toLoad.append(Container((0,0),values['input2'],values['input']))
            window['input'].update('')
            window['input2'].update('')
        elif event == sg.WIN_CLOSED: #Employee clicks the X on the program
            exit()
        window['time'].update(time.strftime('%H:%M:%S')) #Update clock in real time (Military time, local time)

    window.close()
    
def calculate_unload(names,fileName,toLoad,unLoad):
    sg.theme('LightGray1')
    font = ('Arial',30)
    
    layout = [
    [sg.Text(fileName,font = font),sg.Text('',font = font,pad = (200,0),key = 'time'),sg.Text(names,font = font,pad = ((20,0),(0,0)))],
    [sg.Text('',size = (0,3))],
    [sg.Text('Calculating Loading and Unloading of Ship',font = font, size = (0,3))],
    [sg.Text('',size = (0,3))],
    [sg.Button('Comments',size=(10,2),font = ('Arial',14)), sg.Button('Done',pad = (200,0),size = (10,2),font = ('Arial',14)),sg.Button('Login',size=(10,2),font = ('Arial',14))]
    ]
    window = sg.Window('Loading Unloading Page', layout, size=(900, 700),finalize = True)
    initialState = Node()
    initialState.ship = manifest_ship
    initialState.toLoad = toLoad
    initialState.toUnload = unLoad
    finished_state = unload(initialState)
    while True:
        event, values = window.read(timeout = 10)
        if event == 'Login': #Employee clicks Login button
            window.close()
            signin_page(names, fileName, 'calculate unload','',toLoad,unLoad)
        elif event == 'Comments': #Employee clicks Comments button
            window.close()
            comments_page(names,fileName,'calculate unload','',toLoad,unLoad)
        elif event == 'Done':
            window.close()
            moves_page(names,fileName,finished_state)
        elif event == sg.WIN_CLOSED: #Employee clicks the X on the program
            exit()
        window['time'].update(time.strftime('%H:%M:%S')) #Update clock in real time (Military time, local time)

    window.close()
    
    

def balancing_page(names,fileName):
    sg.theme('LightGray1')
    font = ('Arial',30)

    layout = [
    [sg.Text(fileName,font = font),sg.Text('',font = font,pad = (200,0),key = 'time'),sg.Text(names,font = font,pad = ((20,0),(0,0)))],
    [sg.Text('',size = (0,3))],
    [sg.Text('Calculating Balance of Ship',font = font, size = (0,3))],
    [sg.Text('',size = (0,3))],
    [sg.Button('Comments',size=(10,2),font = ('Arial',14)), sg.Button('Done',pad = (200,0),size = (10,2),font = ('Arial',14)),sg.Button('Login',size=(10,2),font = ('Arial',14))]
    ]
    window = sg.Window('Balancing Page', layout, size=(900, 700),finalize = True)
    initialState = Node()
    initialState.ship = manifest_ship
    balanced_result = balance(initialState)
    while True:
        event, values = window.read(timeout = 10)
        if event == 'Login': #Employee clicks Login button
            window.close()
            signin_page(names, fileName, 'balance','','','')
        elif event == 'Comments': #Employee clicks Comments button
            window.close()
            comments_page(names,fileName,'balance','','','')
        elif event == 'Done':
            window.close()
            moves_page(names,fileName,balanced_result)
        elif event == sg.WIN_CLOSED: #Employee clicks the X on the program
            exit()
        window['time'].update(time.strftime('%H:%M:%S')) #Update clock in real time (Military time, local time)

    window.close()

def moves_page(names,fileName, resultNode):
    sg.theme('LightGray1')
    font = ('Arial',30)
    string_node_result = ','.join(str(move) for move in resultNode.moves) #(1,2,1,8) with parenthesis and commas
    string_node_result = re.sub(" ", "", string_node_result)


    list_of_moves = re.findall("-?\d+", string_node_result)

    string_of_moves = ""
    iteration = 1
    for i in list_of_moves:
        if iteration % 2 == 0:
            string_of_moves += i + ")"
            if iteration - 1 < len(list_of_moves)-1:
                string_of_moves += "\n"
        else:
            string_of_moves += "(" + i + ", "
        iteration += 1
    string_of_instructions = ""
    iteration = 1
    for i in string_of_moves.split("\n"):
        if iteration % 2 == 0:
            string_of_instructions += " to " + i
            if iteration - 1 < len(string_of_moves):
                string_of_instructions += "\n"
        else:
            string_of_instructions += "Move " + i
        iteration += 1
    layout = [
    [sg.Text(fileName,font = font),sg.Text('',font = font,pad = (200,0),key = 'time'),sg.Text(names,font = font,pad = ((20,0),(0,0)))],
    [sg.Text(string_of_instructions,font = font)],
    # [sg.Text('',size = (0,3))],
    # [sg.Text('Calculating Balance of Ship',size = (0,3))],
    # [sg.Text('',size = (0,3))],
    [sg.Button('Comments',size=(10,2),font = ('Arial',14)), sg.Button('Done',pad = (200,0),size = (10,2),font = ('Arial',14)),sg.Button('Login',size=(10,2),font = ('Arial',14))]
    ]
    window = sg.Window('Moves Page', layout, size=(900, 700),finalize = True)
    while True:
        event, values = window.read(timeout = 10)
        if event == 'Login': #Employee clicks Login button
            window.close()
            signin_page(names, fileName, 'moves','','','')
        elif event == 'Comments': #Employee clicks Comments button
            window.close()
            comments_page(names,fileName,'moves','','','')
        elif event == 'Done':
            window.close()
            main_page(names,'')
        elif event == sg.WIN_CLOSED: #Employee clicks the X on the program
            exit()
        window['time'].update(time.strftime('%H:%M:%S')) #Update clock in real time (Military time, local time)

    window.close()


def main():
    main_page('','') #First open main page with no employee name and no file name
if __name__ == '__main__':
    main()

