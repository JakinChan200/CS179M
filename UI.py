import PySimpleGUI as sg
from datetime import datetime 

def main_page(name):
    sg.theme('LightGray1')  
    font = ('Arial', 30)   
      
    fileName = 'CanardII.txt'
    names = name
    
    layout = [
        [sg.Text(fileName,font = font,),sg.Text(datetime.now().strftime('%H:%M:%S'),font = font,pad = (200,0)),sg.Text(names,font = font,pad = ((20,0),(0,0)))],                                                                                         
        [sg.Text('',size = (0,15))],
        [sg.Button('Loading/Unloading',size=(10,2),pad = ((50,0),(0,0)),font = font), sg.Button('Balancing',pad = ((125,0),(0,0)),size=(10,2.5),font = font)],
        [sg.Text('',size = (0,15))],
        [sg.Button('Comments',size=(10,2),font = ('Arial',14)), sg.Button('Login',pad = ((550,0),(0,0)),size=(10,2),font = ('Arial',14))]
    ]
    window = sg.Window('GUI page', layout, size=(900, 700))
    while True:
        event, values = window.read()
        if event == 'Login':
            window.close()
            signin_page()
        if event == 'Comments':
            window.close()
            comments_page(name)
        elif event == sg.WIN_CLOSED:
            exit()
    
    window.close()

def signin_page():
    sg.theme('LightGray1')  
    font = ('Arial',15)   
    
    layout = [
    [sg.Text('Sign in',font = font)],
    [sg.Text('Name', font = font), sg.InputText(size=(50,10),expand_y = True)],
    [sg.Submit(), sg.Cancel()]
    ]
  
    window = sg.Window('Sign in page', layout)
    event, values = window.read()
    window.close()   
    main_page(values[0])
    
def comments_page(name):
    sg.theme('LightGray1')  
    font = ('Arial',15)  
    
    layout = [
    [sg.Text("Enter your comment:")],
    [sg.Multiline(size=(50, 20))],
    [sg.Button("Submit")]
    ]
    
    window = sg.Window('Comment page', layout, font = font)
    event, values = window.read()
    window.close() 
    main_page(name)  
    
def main():
    main_page('')
        
if __name__ == '__main__':
    main()
    
    
    