import PySimpleGUI as sg

sg.theme('Kayak')

def clearInput():
        # A list of the inputs we want to clear
       keys_to_clear = ['-Call-', '-Time-', '-RST-', '-County-']
       # This section will clear the inputs and restore defaults
       for key in keys_to_clear:
        window[key]('')
        window['-RST-']('59')
        window['-Mode-']('Phone')
        window['-County-']('')

counties = ['Annapolis', 'Antigonish', 'Cape Breton', 'Colchester', 'Cumberland', 
            'Digby', 'Guysborough','Halifax', 'Hants', 'Inverness', 'Kings', 'Lunenburg', 
            'Pictou', 'Queens', 'Richmond', 'Shelburne', 'Victoria', 'Yarmouth']
modes = ['Phone', 'CW', 'Digital']

layout = [[sg.T('NSARA Contest Logger')],
        [sg.T('Call:'), sg.I(size = (10, 1), k = '-Call-'), sg.T('Time:'), sg.I(size = (10, 1), k = '-Time-'), sg.T('RST:'), 
        sg.I(size = (10, 1), default_text = '59', k = '-RST-'), sg.T('Mode:'), sg.Combo(values = (modes), default_value = 'Phone', enable_events=True, size = (10, 1), k = '-Mode-'), sg.T('County or Serial:'), sg.Combo(values = counties, k = '-County-')],
        [sg.B('Save', tooltip = 'Save this QSO to the log', size = (15,1)), sg.B('Clear', tooltip = 'Clear all fields', size = (15,1)), sg.B('Exit', tooltip = 'Exit the program', size = (15, 1))]]  

window = sg.Window('Logger', layout) 

while True:
    event, values = window.read() 
  
    if event == 'Exit' or event == sg.WIN_CLOSED:
        break
    if event == 'Clear':
        clearInput()
    if event == 'Save':
        if values['-Call-'] != '' and values['-County-'] != '':        
            # Write the QSO to a local file        
            with open("/home/user1/apps/python/PySimpleGUI/Projects/logger/mylog1.csv", "a") as log:
                log.write(values['-Call-'] + ',')
                log.write(values['-Time-'] + ',')
                log.write(values['-RST-'] + ',')
                log.write(values['-Mode-'] + ',')
                log.write(values['-County-'])
            clearInput()
        # Check for empty input
        elif values['-Call-']=='': 
            sg.popup('Callsign cannot be blank.', title = 'OOPS!') 
        elif values['-County-']== '':
            sg.popup('County or Serial cannot be blank.', title = 'OOPS!')       
            
window.close()
#with open("/home/pi/apps/Projects/PySimpleGUI/Temp/cpu_temp1.csv", "a") as log:        
    #    log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(cel_temp)))