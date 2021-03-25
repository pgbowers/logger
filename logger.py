import PySimpleGUI as sg

sg.theme('Kayak')

layout = [[sg.Text('NSARA Contest Logger')],
        [sg.Text('Call:'), sg.Input(key = '-Call-'), sg.Text('Time:'), sg.Input(key = '-Time-')],
        [sg.Text('RST:'), sg.Input(key = '-RST-'), sg.Text('Mode:'), sg.Input(key = '-Mode-')],
        [sg.Text('County or Serial:'), sg.Input(key = '-County-')],
        [sg.Button('Save', size = (15,1)), sg.Button('Cancel', size = (15,1))]]  

window = sg.Window('Logger', layout) 

while True:
    event, values = window.read()
    if event == 'Exit' or event == sg.WIN_CLOSED:
        break

window.close()