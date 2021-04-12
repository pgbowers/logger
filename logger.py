import PySimpleGUI as sg
import pickle
from datetime import datetime

sg.theme('Kayak')

# Declare some variables
countiesWorked = []
QSOCount = 0
score = 0
countyScore = 0

# Get the current system time for the log
now = datetime.now()
current_time = now.strftime("%H:%M")

# load our previously saved data
with open('callFile', 'rb') as f:
    myCall = pickle.load(f)

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

def clearScores():
    # clear the scoring fields and the scores.csv file

    # send a popup first to make sure...
    confirmClear = sg.popup_yes_no('Are you sure?', title = 'Confirm clear scores')    
    if confirmClear == 'No':
        pass
    else:        
        # the global keyword is needed to change QSOCount in this function and have the change apply everywhere.
        global QSOCount, score, countiesWorked, countyScore
        QSOCount = 0
        score = 0
        countyScore = 0
        countiesWorked = []       
        window.Element('-QSO-').update(QSOCount)
        window.Element('-Counties-').update(countyScore)
        window.Element('-Score-').update(score)    
        # erase the contents of the scores file
        with open("/home/user1/apps/python/PySimpleGUI/Projects/logger/scores.csv", "w") as scores:
            scores.truncate(0)

counties = ['Annapolis', 'Antigonish', 'Cape Breton', 'Colchester', 'Cumberland', 
            'Digby', 'Guysborough','Halifax', 'Hants', 'Inverness', 'Kings', 'Lunenburg', 
            'Pictou', 'Queens', 'Richmond', 'Shelburne', 'Victoria', 'Yarmouth']
modes = ['Phone', 'CW', 'Digital']

# A dictionary of calls and modes so we can check for duplicates.
#callDict = {}
callList = []

# ------ Menu Definition ------ #
menu_def = [['&File', ['&Setup', ['Your Callsign', 'Contest Date', ], '&Clear Scores', 'E&xit']],
            ['&Edit', ['&Paste', ['Special', 'Normal', ], 'Undo'], ],            
            ['&Help', '&About...'] 
           ]
# ------------------------------#

layout =[
        [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
        [sg.Frame(layout = [[sg.T('Call:'), sg.I(size = (10, 1), focus = False, k = '-Call-'), sg.T('Time:'), sg.I(default_text = current_time, size = (10, 1), k = '-Time-'), sg.T('RST:'),
        sg.I(size = (10, 1), default_text = '59', k = '-RST-'), sg.T('Mode:'), sg.Combo(values = (modes), default_value = 'Phone', size = (10, 1), k = '-Mode-'), sg.T('County or Serial:'), sg.Combo(values = counties, size = (15,1), k = '-County-')],
        [sg.B('Save', tooltip = 'Save this QSO to the log', size = (15,1), pad = ((80, 0),(20,20))), sg.B('Clear', tooltip = 'Clear all fields', size = (15,1), pad = (80, 0)), sg.B('Exit', tooltip = 'Exit the logger', size = (15, 1), pad = (80, 1))]],title = "Input", pad = ((20, 20),(20, 20)))],
        [sg.Frame(layout = [[sg.T("QSO's: "), sg.T('', size = (5, 1), k = '-QSO-'), sg.T("Counties: "), sg.T('', size = (5, 1),k = '-Counties-'), sg.T("Score: "), sg.T('', size = (5, 1),k = '-Score-')]], title = 'Score', pad = ((20, 20),(0, 20)))],
        [sg.Frame(layout = [[sg.Multiline(default_text='', k = '-LogDisplay-', autoscroll = True, disabled = True, do_not_clear = True, size = (200, 4), background_color = 'white')]], title = 'Your Log', pad = ((20, 20),(0, 20)))]
        ] 
        
window = sg.Window('NSARA Contest Logger for: ' + str(myCall), layout, font = 'Arial', element_justification = 'l', grab_anywhere = True, resizable = True) 
 
while True:
    event, values = window.read()                                                                                              
  
    if event == 'Exit' or event == sg.WIN_CLOSED:
        # Write the scores to a local file for next session      
        with open("/home/user1/apps/python/PySimpleGUI/Projects/logger/scores.csv", "w") as scores:
            scores.write(str(QSOCount) + ',')
            scores.write(str(len(countiesWorked)) + ',')
            scores.write(str(score) + '\n')
            #scores.write('Test123')
        break
    if event == 'Clear':
        clearInput()

    if event == 'About...':
            #window.disappear() # uses alpha channel so doesn't work on Elementary or PI
            sg.popup('NSARA Contest Logger', 'Version 1.0',
            'by Peter Bowers, VE1BZI', no_titlebar = True, grab_anywhere=False)
            #window.reappear() # uses alpha channel so doesn't work on Elementary or PI

    if event == 'Open':
        filename = sg.popup_get_file('file to open', no_window=True)
        print('Open clicked')

    if event == 'Your Callsign':
        callSign = sg.PopupGetText('Enter your Callsign or SWL for shortwave listener', title = 'Your Callsign')
        with open('callFile', 'wb') as f:
            pickle.dump(callSign, f)
        print(callSign)

    if event == 'Clear Scores':        
        clearScores()   
    #**************
    # when the save button is pressed
    if event == 'Save':
        # make sure that the call and county fields have a value in them
        if values['-Call-'] != '' and values['-County-'] != '': 
            #******************
            # build a list of the counties that have been worked
            if not values['-Call-'] in callList:
                callList.append(values['-Call-'])
                #print('Line 118: ' + str(callList))
            #*****************  
             # build a list of the values entered
                logentry = []
                logentry.append(values['-Call-'])
                logentry.append(current_time)
                logentry.append(values['-RST-'])
                logentry.append(values['-Mode-'])
                logentry.append(values['-County-'])
                print('Line 135: ' + str(logentry))

                #[print(*word) for word in logentry]
                #for word in logentry:
                #    window['-LogDisplay-'].update(value = word, append = False, autoscroll = True)

                for word in logentry:
                   print (word, end = ' ')

            #*****************    
            # Write the logentry to a local file        
            with open('mylog.txt', 'ab') as log:            
                pickle.dump(logentry , log)
            #*****************

            with open('mylog.txt', 'rb') as log:
                readout = []
                while True:
                    try:
                        readout.append(pickle.load(log))
                        #window['-LogDisplay-'].update(value = readout, append = False, autoscroll = True)
                        #print(readout)
                    except EOFError: # reached the end of the file
                        break                               
                #print(readout)               
                                       
            #****************
            # Display a runing total of QSO's, new counties worked and total score
            QSOCount+=1            
            window.Element('-QSO-').update(QSOCount)
            if not values['-County-'] in countiesWorked and values['-County-'] in counties:
                countiesWorked.append(values['-County-']) 
                countyScore = len(countiesWorked) 
                #print('Line 114: ' + str(countyScore))              
            window.Element('-Counties-').update(countyScore)
            # if the first log entry is a serial number not a county(multiply by zero)
            if countyScore == 0:
                score = QSOCount + countyScore
            else:
                score = QSOCount * countyScore
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