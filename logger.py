import PySimpleGUI as sg

sg.theme('Kayak')

def clearInput():
        # A list of the inputs we want to clear
       keys_to_clear = ['-Call-', '-Time-', '-RST-']
       # This section will clear the inputs and restore defaults
       for key in keys_to_clear:
        window[key]('')
        window['-RST-']('59')
        window['-Mode-'](modes)
        window['-County-'](counties)


counties = ('Annapolis', 'Digby', 'Hants', 'Inverness')
modes = ('Phone', 'CW', 'Digital')

layout = [[sg.T('NSARA Contest Logger')],
        [sg.T('Call:'), sg.I(size = (10, 1), k = '-Call-'), sg.T('Time:'), sg.I(size = (10, 1), k = '-Time-'), sg.T('RST:'), sg.I(size = (10, 1), default_text = '59', k = '-RST-'), sg.T('Mode:'), sg.Listbox(values = (modes), default_values = 'Phone', select_mode = 'LISTBOX_SELECT_MODE_SINGLE', bind_return_key = True, size = (10, 1), k = '-Mode-'), sg.T('County or Serial:'), sg.Listbox(values = counties, k = '-County-')],
        [sg.B('Save', tooltip = 'Save this QSO to the log', size = (15,1)), sg.B('Clear', tooltip = 'Clear all fields', size = (15,1)), sg.B('Exit', tooltip = 'Exit the program', size = (15, 1))]]  

window = sg.Window('Logger', layout) 

while True:
    event, values = window.read()
    for i in values:
        print(values[i])
    if event == 'Exit' or event == sg.WIN_CLOSED:
        break
    if event == 'Clear':
        clearInput()
    if event == 'Save':
        with open("/home/user1/apps/python/PySimpleGUI/Projects/logger/mylog1.csv", "a") as log:
                for item in values:
                        log.write(str(values[item]) + ',')
                clearInput()

window.close()
#with open("/home/pi/apps/Projects/PySimpleGUI/Temp/cpu_temp1.csv", "a") as log:        
    #    log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(cel_temp)))