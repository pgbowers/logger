import PySimpleGUI as sg

sg.theme('Kayak')

counties = ('Annapolis', 'Digby', 'Hants', 'Inverness')

layout = [[sg.T('NSARA Contest Logger')],
        [sg.T('Call:'), sg.I(k = '-Call-'), sg.T('Time:'), sg.I(k = '-Time-')],
        [sg.T('RST:'), sg.I(k = '-RST-'), sg.T('Mode:'), sg.Listbox(values = ('Phone', 'CW', 'Digital'), default_values = 'Phone', select_mode = 'LISTBOX_SELECT_MODE_SINGLE', bind_return_key = True, size = (15, 1), k = '-Mode-')],
        [sg.T('County or Serial:'), sg.Listbox(values = counties, k = '-County-')],
        [sg.B('Save', tooltip = 'Save this QSO to the log', size = (15,1)), sg.B('Clear', tooltip = 'Clear all fields', size = (15,1))]]  

window = sg.Window('Logger', layout) 

while True:
    event, values = window.read()
    if event == 'Exit' or event == sg.WIN_CLOSED:
        break

window.close()