import PySimpleGUI as sg
import pickle
import csv
from datetime import datetime

sg.theme('Kayak')

# Declare some variables
countiesWorked = []
QSOCount = 0
score = 0
countyScore = 0
data = []

# Get the current system time for the log
now = datetime.now()
current_time = now.strftime("%H:%M")

# load our previously saved data
#with open('call.txt', 'rb') as f:
#    myCall = pickle.load(f)

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
#***********************************
# get the log to display in the table
def displayContacts():
    with open("/home/user1/apps/python/PySimpleGUI/Projects/logger/mylog1.csv", 'r') as infile:
        reader = csv.reader(infile)
        try:
            data = list(reader) # read the file into a list of rows
            print('Line 60: ', data)
        except:
            sg.popup_error('Error reading file')
        return data
#************************************


counties = ['Annapolis', 'Antigonish', 'Cape Breton', 'Colchester', 'Cumberland', 
            'Digby', 'Guysborough','Halifax', 'Hants', 'Inverness', 'Kings', 'Lunenburg', 
            'Pictou', 'Queens', 'Richmond', 'Shelburne', 'Victoria', 'Yarmouth']
modes = ['Phone', 'CW', 'Digital']
headings = ['Call', 'Time', 'RST', 'Mode', 'County or Serial#']

# A dictionary of calls and modes so we can check for duplicates.
#callDict = {}
callList = []

# ------ Menu Definition ------ #
menu_def = [['&File', ['&Setup', ['Your Callsign', 'Contest Date', ], '&Clear Scores', 'E&xit']],
            ['&Edit', ['&Paste', ['Special', 'Normal', ], 'Undo'], ],            
            ['&Help', '&About...'] 
           ]
# ------------------------------#
#displayContacts()

#print('Line 82:', data)

layout =[
        [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
        [sg.Frame(layout = [[sg.T('Call:'), sg.I(size = (10, 1), focus = False, k = '-Call-'), sg.T('Time:'), sg.I(default_text = current_time, size = (10, 1), k = '-Time-'), sg.T('RST:'),
        sg.I(size = (10, 1), default_text = '59', k = '-RST-'), sg.T('Mode:'), sg.Combo(values = (modes), default_value = 'Phone', size = (10, 1), k = '-Mode-'), sg.T('County or Serial:'), sg.Combo(values = counties, size = (15,1), k = '-County-')],
        [sg.B('Save', tooltip = 'Save this QSO to the log', size = (15,1), pad = ((80, 0),(20,20))), sg.B('Clear', tooltip = 'Clear all fields', size = (15,1), pad = (80, 0)), sg.B('Exit', tooltip = 'Exit the logger', size = (15, 1), pad = (80, 1))]],title = "Input", pad = ((20, 20),(20, 20)))],
        [sg.Frame(layout = [[sg.T("QSO's: "), sg.T('', size = (5, 1), k = '-QSO-'), sg.T("Counties: "), sg.T('', size = (5, 1),k = '-Counties-'), sg.T("Score: "), sg.T('', size = (5, 1),k = '-Score-')]], title = 'Score', pad = ((20, 20),(0, 20)))],       
        [sg.Table(values=displayContacts(), headings=headings, max_col_width=25,
            # background_color='light blue',
            auto_size_columns=False,
            display_row_numbers=True,
            justification='center',
            def_col_width = 15,
            num_rows=10,
            alternating_row_color='lightyellow',
            key='-Table-',
            row_height=35,
            tooltip='This is a table')],
          [sg.Button('Change Colors')],          
          [sg.Text('Change Colors = Changes the colors of rows 8 and 9')],
        ] 
        
window = sg.Window('NSARA Contest Logger for: ' + str('ve1bzi'), layout, font = 'Arial', element_justification = 'l', grab_anywhere = True, resizable = True) 
 
while True:
    event, values = window.read()  

    #displayContacts()                                                                                            
  
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
        with open('call.txt', 'wb') as f:
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
                print('Line 135: ', logentry)

                #[print(*word) for word in logentry]
                #for i in logentry:
                    #word = *i
                #data.append([list(logentry)])
                #print('Line 169: ', data)
                #***************************************
                # add each log entry to the .csv file (Apr 18)
                with open("/home/user1/apps/python/PySimpleGUI/Projects/logger/mylog1.csv", 'a') as infile:
                    writer = csv.writer(infile)
                    writer.writerow(logentry)
                #***************************************

                # This will display the refreshed table after each entry
                window['-Table-'].Update(values=displayContacts())

                # This will write  only the last entry to the table
                #window['-Table-'].Update(values=[list(logentry)])
                    
                #print('Line 136: ' + str(logentry))
                                                  
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