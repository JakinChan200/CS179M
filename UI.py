import time
import datetime as dt
from readManifest import *
import PySimpleGUI as sg


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
        [sg.Button('Loading/Unloading',size=(10,2),pad = ((50,0),(0,0)),font = font), sg.Button('Balancing',pad = ((125,0),(0,0)),size=(10,2.5),font = font)],
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
            signin_page(name,fileName,'main')
        elif event == 'Comments': #Employee clicks Comments button
            window.close()
            comments_page(name, fileName, 'main')
        elif event == 'Loading/Unloading': #Employee clicks Loading/Unloading button
            window.close()
            unloading_loading_page(name,fileName)
        elif event == 'Balancing': #Employee clicks Balancing button
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
    openFile()
    writeToLog(logfile,getFileName() + " has been uploaded")
    main_page(name,getFileName())


def signin_page(name, fileName, function_call): #function_call tells which function is calling this function
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


def comments_page(name, fileName,function_call): #function_call tells which function is calling this function
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

def unloading_loading_page(names,fileName):
    sg.theme('LightGray1')
    font = ('Arial',30)

    layout = [
    [sg.Text(fileName,font = font),sg.Text('',font = font,pad = (200,0),key = 'time'),sg.Text(names,font = font,pad = ((20,0),(0,0)))],
    [sg.Text('',size = (0,3))],
    [[sg.B('',size=(3,1.125),pad = (0.1,0), key=(i,j)) for i in range (8)] for j in range(12)],
    [sg.Text('',size = (0,3))],
    [sg.Button('Comments',size=(10,2),font = ('Arial',14)), sg.Button('Done',pad = (200,0),size = (10,2),font = ('Arial',14)),sg.Button('Login',size=(10,2),font = ('Arial',14))]
    ]

    window = sg.Window('Loading Unloading Page', layout, size=(900, 700),finalize = True)
    while True:
        event, values = window.read(timeout = 10)
        if event == 'Login': #Employee clicks Login button
            window.close()
            signin_page(names, fileName, 'load unload')
        elif event == 'Comments': #Employee clicks Comments button
            window.close()
            comments_page(names,fileName,'load unload')
        elif event == sg.WIN_CLOSED: #Employee clicks the X on the program
            exit()
        window['time'].update(time.strftime('%H:%M:%S')) #Update clock in real time (Military time, local time)

        #TODO add implementation for done button
    window.close()

def balancing_page(names,fileName):
    sg.theme('LightGray1')
    font = ('Arial',30)

    layout = [
    [sg.Text(fileName,font = font),sg.Text('',font = font,pad = (200,0),key = 'time'),sg.Text(names,font = font,pad = ((20,0),(0,0)))],
    [sg.Text('',size = (0,3))],
    [[sg.B('',size=(3,1.125),pad = (0.1,0), key=(i,j)) for i in range (8)] for j in range(12)],
    [sg.Text('',size = (0,3))],
    [sg.Button('Comments',size=(10,2),font = ('Arial',14)), sg.Button('Done',pad = (200,0),size = (10,2),font = ('Arial',14)),sg.Button('Login',size=(10,2),font = ('Arial',14))]
    ]

    window = sg.Window('Balancing Page', layout, size=(900, 700),finalize = True)
    while True:
        event, values = window.read(timeout = 10)
        if event == 'Login': #Employee clicks Login button
            window.close()
            signin_page(names, fileName, 'balance')
        elif event == 'Comments': #Employee clicks Comments button
            window.close()
            comments_page(names,fileName,'balance')
        elif event == sg.WIN_CLOSED: #Employee clicks the X on the program
            exit()
        window['time'].update(time.strftime('%H:%M:%S')) #Update clock in real time (Military time, local time)

        #TODO add implementation for done button
    window.close()


def main():
    main_page('','') #First open main page with no employee name and no file name
if __name__ == '__main__':
    main()
