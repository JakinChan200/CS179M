import time
import PySimpleGUI as sg

def main_page(name):
    sg.theme('LightGray1')  #Can change theme https://www.geeksforgeeks.org/themes-in-pysimplegui/
    font = ('Arial', 30)   
      
    fileName = 'CanardII.txt' #Change later to read in manifest name
    names = name #Name of the employee logging in, passed in as argument of function
    
    layout = [
        [sg.Text(fileName,font = font,),sg.Text('',font = font,pad = (200,0),key = 'time'),sg.Text(names,font = font,pad = ((20,0),(0,0)))],      
        #File name on top left, Time in the center, and employee name at the right
        #Employee Name is blank before anyone logs in
        [sg.Text('',size = (0,15))],
        #Empty Line for Spacing
        [sg.Button('Loading/Unloading',size=(10,2),pad = ((50,0),(0,0)),font = font), sg.Button('Balancing',pad = ((125,0),(0,0)),size=(10,2.5),font = font)],
        #Loading and Unloading button the left, Balancing button on the right
        [sg.Text('',size = (0,15))],
        [sg.Button('Comments',size=(10,2),font = ('Arial',14)), sg.Button('Login',pad = ((550,0),(0,0)),size=(10,2),font = ('Arial',14))]
        #Comments button on the bottom left, Log in button on the bottom right
    ]

    window = sg.Window('Main page', layout, size=(900, 700),finalize = True)
    
    while True:
        event, values = window.read(timeout=10) #Timeout is required for updating clock
        if event == 'Login': #Employee clicks Login button
            window.close()
            signin_page()
        if event == 'Comments': #Employee clicks Comments button
            window.close()
            comments_page(name)
        elif event == sg.WIN_CLOSED: #Employee clicks the X on the program
            exit()
        window['time'].update(time.strftime('%H:%M:%S')) #Update clock in real time (Military time, local time)
            
        #TODO: Add implementation and pages for Loading/Unloading Buttons and Balancing Button
    
    window.close()

def signin_page():
    sg.theme('LightGray1')  #Can change theme https://www.geeksforgeeks.org/themes-in-pysimplegui/
    font = ('Arial',15)   
    
    layout = [
    [sg.Text('Sign in',font = font)],
    [sg.Text('Name', font = font), sg.InputText(size=(50,10),expand_y = True)], #Text box for signing in
    [sg.Submit(), sg.Cancel()] #Submit button and hitting enter both submits the text
    ]
  
    window = sg.Window('Sign in page', layout)
    event, values = window.read()
    window.close()   
    main_page(values[0]) #Open the main page after closing the sign in page, passing in the name typed in as argument
    
def comments_page(name):
    sg.theme('LightGray1')  #Can change theme https://www.geeksforgeeks.org/themes-in-pysimplegui/
    font = ('Arial',15)  
    
    layout = [
    [sg.Text("Enter your comment:")],
    [sg.Multiline(size=(50, 20))], #Multi-line input box, employee has to click "Submit" to submit the comment, enter does not submit
    [sg.Button("Submit")]
    ]
    
    window = sg.Window('Comment page', layout, font = font)
    event, values = window.read()
    window.close() 
    main_page(name)   #Open the main page after closing the comments page, passing in the name typed in as argument
    #TODO: Add variable to store the comments made
    
def main():
    main_page('') #First open main page with no employee name
        
if __name__ == '__main__':
    main()
    
    
    