import time
import datetime as dt
import math
from readManifest import *
from algorithm import *
import PySimpleGUI as sg
from updateManifest import *

manifest_ship = []

logfile = "Logfile_2022.txt" #temp var-- change to ask file name when program starts
uploaded = False
signedIn = False
save_path = ''
newname = ''

def writeToLog (fileName, comment):
    date = dt.datetime.now()
    file = open(fileName, 'a')
    file.write(date.strftime('%B %d, %Y') + ": " + time.strftime('%H:%M:%S') + ' ' ) #https://www.programiz.com/python-programming/datetime/strftime
    file.write(comment)
    file.write('\n')
    file.close()

def start_page():
    global logfile
    global save_path
    sg.theme('LightGray1')  #Can change theme https://www.geeksforgeeks.org/themes-in-pysimplegui/
    font = ('Arial',15)

    layout = [
    [sg.Text('Enter log file name and path to desktop',font = font)],
    [sg.Text('Log File Name', font = font), sg.InputText(size=(50,10),expand_y = True)], 
    [sg.Text('Path to Desktop', font = font), sg.InputText(size=(50,10),expand_y = True)],#Text box for signing in
    [sg.Submit(), sg.Cancel()] #Submit button and hitting enter both submits the text
    ]
    window = sg.Window('Start Page', layout)
    event, values = window.read()
    logfile = values[0] + ".txt"
    if event == 'Cancel':
        exit()
    save_path = values[1]
    window.close()
    main_page('','')
    

def main_page(name, fileName):
    global uploaded
    global signedIn
    global newname
    sg.theme('LightGray1')  #Can change theme https://www.geeksforgeeks.org/themes-in-pysimplegui/
    font = ('Arial', 30)

    names = name #Name of the employee logging in, passed in as argument of function
    layout = [
        [sg.Text(fileName,font = font),sg.Text('',font = font,pad = (200,0),key = 'time'),sg.Text(names,font = font,pad = ((20,0),(0,0)))],
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
    newname = names
    while True:
        event, values = window.read(timeout=10) #Timeout is required for updating clock 
        #https://gist.github.com/KenoLeon/907a4df79e5be20a1ffb37617f00d2e4
        if event == 'Login': #Employee clicks Login button
            window.close()
            signin_page(name,fileName,'main','','','','')
        elif event == 'Comments': #Employee clicks Comments button
            window.close()
            comments_page(name, fileName, 'main','','','','')
        elif event == 'Load/Unload': #Employee clicks Loading/Unloading button
            if uploaded and signedIn:
                window.close()
                unloading_loading_page(name,fileName)
        elif event == 'Balance': #Employee clicks Balancing button
            if uploaded and signedIn:
                window.close()
                balancing_page(name,fileName)
        elif event == 'Upload': #Employee clicks Upload to upload manifest
            window.close()
            upload_file(name)
        elif event == sg.WIN_CLOSED: #Employee clicks the X on the program
            exit()
        window['time'].update(time.strftime('%H:%M:%S')) #Update clock in real time (Military time, local time)
        #https://gist.github.com/KenoLeon/907a4df79e5be20a1ffb37617f00d2e4

    window.close()

def upload_file(name):
    global uploaded
    global manifest_ship
    count = 0
    manifest_ship = openFile()
    for container in manifest_ship:
        if container.name != 'NAN' and container.name != 'UNUSED':
            count += 1
    writeToLog(logfile,getFileName() + " has been uploaded, there are " + str(count) + " containers on the ship")
    uploaded = True
    main_page(name,getFileName())


def signin_page(name, fileName, function_call,containers_to_unload,toLoad,unLoad,resultNode): #function_call tells which function is calling this function
    global signedIn
    global newname
    sg.theme('LightGray1')  #Can change theme https://www.geeksforgeeks.org/themes-in-pysimplegui/
    font = ('Arial',15)

    layout = [
    [sg.Text('Sign in',font = font)],
    [sg.Text('Name', font = font), sg.InputText(size=(50,10),expand_y = True)], #Text box for signing in
    [sg.Submit(), sg.Cancel()] #Submit button and hitting enter both submits the text
    ]
    signedIn = True
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
        newname = values[0]
    elif function_call == 'calculate unload':
        newname = values[0]
    elif function_call == 'moves':
        moves_page(values[0],fileName,resultNode)
    elif function_call == 'load page':
        load_page(values[0],fileName,containers_to_unload)
    elif function_call == 'success':
        success_page(values[0],fileName)


def comments_page(name, fileName,function_call,containers_to_unload,toLoad,unLoad,resultNode): #function_call tells which function is calling this function
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
    elif function_call == 'moves':
        moves_page(name,fileName,resultNode)
    elif function_call == 'load page':
        load_page(name,fileName,containers_to_unload)
    elif function_call == 'success':
        success_page(name,fileName)

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
    #https://www.tutorialspoint.com/pysimplegui/pysimplegui_listbox_element.htm
    layout = [
    [sg.Text(fileName,font = font),sg.Text('',font = font,pad = (200,0),key = 'time'),sg.Text(names,font = font,pad = ((20,0),(0,0)))],
    [sg.Text('Select Containers to Unload',font = font,size = (0,1))],
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
            signin_page(names, fileName, 'load unload','','','','')
        elif event == 'Comments': #Employee clicks Comments button
            window.close()
            comments_page(names,fileName,'load unload','','','','')
        elif event == 'Done':
            window.close()
            containers_to_unload = values['-LIST-']
            load_page(names,fileName,containers_to_unload)
        elif event == sg.WIN_CLOSED: #Employee clicks the X on the program
            exit()
        window['time'].update(time.strftime('%H:%M:%S')) #Update clock in real time (Military time, local time)

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
    [sg.Text('',size = (800,28))],
    [sg.Button('Comments',size=(10,2),font = ('Arial',14)), sg.Button('Done',pad = (200,0),size = (10,2),font = ('Arial',14)),sg.Button('Login',size=(10,2),font = ('Arial',14))]
    ]
    window = sg.Window('Load Page', layout, size=(900, 700),finalize = True)

    while True:
        event, values = window.read(timeout = 10)
        if event == 'Login': #Employee clicks Login button
            window.close()
            signin_page(names, fileName, 'load page',containers_to_unload,'','','')
        elif event == 'Comments': #Employee clicks Comments button
            window.close()
            comments_page(names,fileName,'load page',containers_to_unload,'','','')
        elif event == 'Done':
            window.close()
            calculate_unload(names,fileName,toLoad,containers_to_unload)
        elif event == 'Add container':
            toLoad.append(Container((0,0),int(values['input2']),values['input']))
            window['input'].update('')
            window['input2'].update('')
        elif event == sg.WIN_CLOSED: #Employee clicks the X on the program
            exit()
        window['time'].update(time.strftime('%H:%M:%S')) #Update clock in real time (Military time, local time)

    window.close()

def calculate_unload(names,fileName,toLoad,unLoad):
    global newname
    sg.theme('LightGray1')
    font = ('Arial',30)

    layout = [
    [sg.Text(fileName,font = font),sg.Text('',font = font,pad = (200,0),key = 'time'),sg.Text(names,font = font,pad = ((20,0),(0,0)),key = "login")],
    [sg.Text('',size = (0,3))],
#     [sg.Text('Calculating Loading and Unloading of Ship',font = font, size = (0,3))],
    [sg.Text('Estimated Time (At Most):',font = font, size = (0,1))],
    [sg.Text('',font = font, size = (800,1), key = 'estimation')],
    [sg.Text('',size = (800,35))],
    [sg.Button('Comments',size=(10,2),font = ('Arial',14)), sg.Button('Done',pad = (200,0),size = (10,2),font = ('Arial',14)),sg.Button('Login',size=(10,2),font = ('Arial',14))]
    ]
    window = sg.Window('Calculate Unload Page', layout, size=(900, 700),finalize = True)
    initialState = Node()
    initialState.ship = manifest_ship
    initialState.toLoad = toLoad
    initialState.toUnload = unLoad
    finished_state = unload(initialState)
    shortenedfileName = copy.deepcopy(fileName)
    shortenedfileName = shortenedfileName[:-4]
    print(finished_state)
    writeManifest(shortenedfileName, finished_state.ship,save_path)
    times = estimate_time(finished_state.moves)
    hours = math.floor(times/60)
    minutes = times % 60
    while True:
        event, values = window.read(timeout = 10)
        if event == 'Login': #Employee clicks Login button
            signin_page(names, fileName, 'calculate unload','',finished_state.toLoad,finished_state.toUnload,'')
        elif event == 'Comments': #Employee clicks Comments button
            comments_page(names,fileName,'calculate unload','',finished_state.toLoad,finished_state.toUnload,'')
        elif event == 'Done':
            window.close()
            moves_page(newname,fileName,finished_state)
        elif event == sg.WIN_CLOSED: #Employee clicks the X on the program
            exit()
        
        window['time'].update(time.strftime('%H:%M:%S')) #Update clock in real time (Military time, local time)
        window['estimation'].update(str(hours) + ' hours ' + str(minutes) + ' minutes' )
        window['login'].update(newname)

    window.close()

def balancing_page(names,fileName):
    global newname
    sg.theme('LightGray1')
    font = ('Arial',30)

    layout = [
    [sg.Text(fileName,font = font),sg.Text('',font = font,pad = (200,0),key = 'time'),sg.Text(names,font = font,pad = ((20,0),(0,0)),key = 'login')],
    [sg.Text('',size = (0,3))],
#     [sg.Text('Calculating Balance of Ship',font = font, size = (0,3))],
    [sg.Text('Estimated Time (At Most):',font = font, size = (0,1))],
    [sg.Text('',font = font, size = (800,1), key = 'estimation')],
    [sg.Text('',size = (800,35))],
    [sg.Button('Comments',size=(10,2),font = ('Arial',14)), sg.Button('Done',pad = (200,0),size = (10,2),font = ('Arial',14)),sg.Button('Login',size=(10,2),font = ('Arial',14))]
    ]
    window = sg.Window('Balancing Page', layout, size=(900, 700),finalize = True)
    initialState = Node()
    initialState.ship = manifest_ship
    balanced_result = balance(initialState)
    shortenedfileName = copy.deepcopy(fileName)
    shortenedfileName = shortenedfileName[:-4]
    writeManifest(shortenedfileName, balanced_result.ship,save_path)
    times = estimate_time(balanced_result.moves)
    hours = math.floor(times/60)
    minutes = times % 60
    while True:
        event, values = window.read(timeout = 10)
        if event == 'Login': #Employee clicks Login button
            signin_page(names, fileName, 'balance','','','','')
        elif event == 'Comments': #Employee clicks Comments button
            comments_page(names,fileName,'balance','','','','')
        elif event == 'Done':
            window.close()
            moves_page(newname,fileName,balanced_result)
        elif event == sg.WIN_CLOSED: #Employee clicks the X on the program
            exit()
        window['time'].update(time.strftime('%H:%M:%S')) #Update clock in real time (Military time, local time)
        window['estimation'].update(str(hours) + ' hours ' + str(minutes) + ' minutes' )
        window['login'].update(newname)



    window.close()

def success_page(names, fileName):
    global uploaded
    sg.theme('LightGray1')
    font = ('Arial',30)
    shortenedfileName = copy.deepcopy(fileName)
    shortenedfileName = shortenedfileName[:-4]
    outboundFileName = shortenedfileName + '_OUTBOUND.txt'
    writeToLog(logfile,"Finished a Cycle. Manifest " + outboundFileName + " was written to desktop, and a reminder to operator to send file was displayed.")
    layout = [
    [sg.Text(fileName,font = font),sg.Text('',font = font,pad = (200,0),key = 'time'),sg.Text(names,font = font,pad = ((20,0),(0,0)))],
    [sg.Text('',size = (0,5))],
    [sg.Text('Success! No more moves to make.',size = (0,3), font = ('Arial 25'), pad = (210,0))],
    [sg.Text('',size = (0,5))],
    [sg.Text('Please email ' + outboundFileName + ' to the captain.',size = (0,3), font = ('Arial 25'),pad = (125,0))],
    [sg.Text('',size = (0,5))],
    [sg.Text(outboundFileName + ' is available on the Desktop.',size = (0,3), font = ('Arial 15'),pad = (250,0))],
    [sg.Text('',size = (0,5))],
    [sg.Button('Comments',size=(10,2),font = ('Arial',14)), sg.Button('Done',pad = (200,0),size = (10,2),font = ('Arial',14)),sg.Button('Login',size=(10,2),font = ('Arial',14))]
    ]
    
    window = sg.Window('Success Page', layout, size=(900, 700),finalize = True)
    while True:
        event, values = window.read(timeout = 10)
        if event == 'Login': #Employee clicks Login button
            window.close()
            signin_page(names, fileName, 'success','','','','')
        elif event == 'Comments': #Employee clicks Comments button
            window.close()
            comments_page(names,fileName,'success','','','','')
        elif event == sg.WIN_CLOSED: #Employee clicks the X on the program
            exit()
        elif event == 'Done':
            window.close()
            uploaded = False
            main_page(names, '')
        window['time'].update(time.strftime('%H:%M:%S')) #Update clock in real time (Military time, local time)

    window.close()

def moves_page(names,fileName, resultNode):
    sg.theme('LightGray1')
    font = ('Arial',30)
    curr_move = 0
    if len(resultNode.moves) != 0:
        string_node_result = ','.join(str(move) for move in resultNode.moves) #(1,2,1,8) with parenthesis and commas
        #https://stackoverflow.com/questions/5618878/how-to-convert-list-to-string
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
    else:
        string_of_instructions = "No Moves\n"
    list_of_instructions = re.findall("[^\n]+\n", string_of_instructions) #list of strings that have instructions
#     print(list_of_instructions)

    layout = [
    [sg.Text(fileName,font = font),sg.Text('',font = font,pad = (200,0),key = 'time'),sg.Text(names,font = font,pad = ((20,0),(0,0)))],
    [sg.Text(list_of_instructions[curr_move],font = font,size = (800,15), key = 'Update moves')],
    # [sg.Text('',size = (0,3))],
    # [sg.Text('Calculating Balance of Ship',size = (0,3))],
    # [sg.Text('',size = (0,3))],
    [sg.Button('Next Move', size=(10,1), font = ('Arial',14))],
    [sg.Button('Comments',size=(10,2),font = ('Arial',14)), sg.Button('Done',pad = (200,0),size = (10,2),font = ('Arial',14)),sg.Button('Login',size=(10,2),font = ('Arial',14))]
    ]
    window = sg.Window('Moves Page', layout, size=(900, 700),finalize = True)
    writeToLog(logfile, list_of_instructions[curr_move][:-1])
    while True:
        event, values = window.read(timeout = 10)
        if event == 'Login': #Employee clicks Login button
            window.close()
            signin_page(names, fileName, 'moves','','','',resultNode)
        elif event == 'Comments': #Employee clicks Comments button
            window.close()
            comments_page(names,fileName,'moves','','','',resultNode)
        elif event == 'Done':
            window.close()
            success_page(names,fileName)
        elif event == 'Next Move':
            if curr_move < len(list_of_instructions) - 1:
                curr_move += 1
                writeToLog(logfile, list_of_instructions[curr_move][:-1])
                window['Update moves'].update(list_of_instructions[curr_move])
            else:
                window['Update moves'].update("No more moves to make.")
        elif event == sg.WIN_CLOSED: #Employee clicks the X on the program
            exit()
        window['time'].update(time.strftime('%H:%M:%S')) #Update clock in real time (Military time, local time)

    window.close()

def main():
    start_page()
#     main_page('','') #First open main page with no employee name and no file name
    # success_page('Ash', 'Login.txt') #Testing Success page
if __name__ == '__main__':
    main()
