import PySimpleGUI as sg
from datetime import datetime

sg.theme('Kayak')

# Get the current system time for the log
now = datetime.now()
current_time = now.strftime("%H:%M")

def clearInput():
        # A list of the inputs we want to clear
       keys_to_clear = ['-Call-', '-RST-', '-County-']
       # This section will clear the inputs and restore defaults
       for key in keys_to_clear:
        window[key]('')
        #window['-Time-']('')
        window['-RST-']('59')
        window['-Mode-']('Phone')
        window['-County-']('')

counties = ['Annapolis', 'Antigonish', 'Cape Breton', 'Colchester', 'Cumberland', 
            'Digby', 'Guysborough','Halifax', 'Hants', 'Inverness', 'Kings', 'Lunenburg', 
            'Pictou', 'Queens', 'Richmond', 'Shelburne', 'Victoria', 'Yarmouth']
modes = ['Phone', 'CW', 'Digital']

QSOCount = 0
countiesWorked = []
score = 0
# A dictionary of calls and modes so we can check for duplicates.
#callDict = {}
callList = []

layout = [[sg.T('NSARA Contest Logger', size = (60,2), justification='right')],
        [sg.T('Call:'), sg.I(size = (10, 1), focus = False, k = '-Call-'), sg.T('Time:'), sg.I(default_text = current_time, size = (10, 1), k = '-Time-'), sg.T('RST:'), 
        sg.I(size = (10, 1), default_text = '59', k = '-RST-'), sg.T('Mode:'), sg.Combo(values = (modes), default_value = 'Phone', size = (10, 1), k = '-Mode-'), sg.T('County or Serial:'), sg.Combo(values = counties, size = (15,1), k = '-County-')],
        [sg.B('Save', tooltip = 'Save this QSO to the log', size = (15,1)), sg.B('Clear', tooltip = 'Clear all fields', size = (15,1)), sg.B('Exit', tooltip = 'Exit the program', size = (15, 1))],
        [sg.T("QSO's: "), sg.T('', size = (5, 1), k = '-QSO-'), sg.T("Counties: "), sg.T('', size = (5, 1),k = '-Counties-'), sg.T("Score: "), sg.T('', size = (5, 1),k = '-Score-')],
        [sg.Multiline(default_text='Hello list!!', background_color = 'white')]]   
          
window = sg.Window('Logger', layout, grab_anywhere = True) 

while True:
    event, values = window.read() 
  
    if event == 'Exit' or event == sg.WIN_CLOSED:
        # Write the scores to a local file for next session      
        with open("/home/user1/apps/python/PySimpleGUI/Projects/logger/scores.csv", "a") as scores:
            scores.write(str(QSOCount) + ',')
            scores.write(str(len(countiesWorked)) + ',')
            scores.write(str(score) + '\n')
            #scores.write('Test123')
        break
    if event == 'Clear':
        clearInput()

    if event == 'Save':
        if values['-Call-'] != '' and values['-County-'] != '': 
            
            if not values['-Call-'] in callList:
                callList.append(values['-Call-'])
                print(callList)
            #*****************       
            # Write the QSO to a local file        
            with open("/home/user1/apps/python/PySimpleGUI/Projects/logger/mylog1.csv", "a") as log:
                log.write(values['-Call-'] + ',')
                log.write(current_time + ',')                
                log.write(values['-RST-'] + ',')
                log.write(values['-Mode-'] + ',')
                log.write(values['-County-'] + '\n')          
            #****************
            # Display a runing total of QSO's, new counties worked and total score
            QSOCount+=1
            window.Element('-QSO-').update(QSOCount)
            if not values['-County-'] in countiesWorked and values['-County-'] in counties:
                countiesWorked.append(values['-County-'])                
            window.Element('-Counties-').update(len(countiesWorked))
            score = QSOCount * len(countiesWorked)
            window.Element('-Score-').update(score)
            #***************
            window.Element('-Time-').update(current_time)            
            clearInput()
            #**************
        # Check for duplicate call signs
        elif values['-Call-'] in callList:
            print(callList)
            sg.popup('Possible Dupe depending on Mode!', background_color='yellow')
            
        # Check for empty input
        elif values['-Call-']=='': 
            sg.popup('Callsign cannot be blank.') 
        else: # values['-County-']== '':
            sg.popup('County or Serial cannot be blank.') 
        #***************            
window.close()