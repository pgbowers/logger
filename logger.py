import PySimpleGUI as sg
import csv
import pandas as pd
import datetime
from io import StringIO

sg.theme('Kayak')

# Declare some variables
countiesWorked = []
QSOCount = 0
score = 0
countyScore = 0
data = []
contest_date = ''
callSign = []
# A list of calls and modes so we can check for duplicates.
callList = []

# Get the current system time for the log
now = datetime.datetime.now()
current_time = now.strftime("%H:%M")

# load our previously saved callsign.
try:
    with open('call.csv', 'r') as call_file:
        myCall = csv.reader(call_file)
        # Convert the .csv to a single string and make it uppercase.   
        for row in myCall:
            callSign = f'{row[0].upper()}'
except IOError:
    fileCreate = sg.popup_ok('Call Sign not found, click OK to create')
    if fileCreate == 'OK':
        with open('call.csv', 'w'):
            pass
# -----------------------------------------

# ----------------------------------------
# load our previously saved contest date.
try:
    with open('date.csv', 'r') as date_file:
        myDate = csv.reader(date_file)
        # Convert the .csv to a single string and make it uppercase.   
        for row in myDate:
            contest_date = f'{row[0].upper()}'
except IOError:
    fileCreate = sg.popup_ok('Date File not found, click OK to create')
    if fileCreate == 'OK':
        with open('date.csv', 'w'):
            pass
# -----------------------------------------

# ----------------------------------------
# load our previously saved score data.
try:
    with open('scores.csv', 'r') as score_file:
        myScores = csv.reader(score_file)
        # Convert the .csv to a single string and make it uppercase.   
        for row in myScores:
            QSOCount = int(row[0])           
            score = int(row[1])
except IOError:
    fileCreate = sg.popup_ok('Date File not found, click OK to create')
    if fileCreate == 'OK':
        with open('date.csv', 'w'):
            pass
# -----------------------------------------
# ----------------------------------------
#load the previously saved list of Counties worked.
try:
    with open('counties.txt', 'r') as file1:
        for line in file1:           
            countiesWorked.append(line.strip('\n'))   
except IOError:
    fileCreate = sg.popup_ok('County File not found, click OK to create')
    if fileCreate == 'OK':
        with open('counties.csv', 'w'):
            pass
# -----------------------------------------
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
        global QSOCount, score, countyScore        
        QSOCount = 0
        score = 0
        countyScore = 0
        countiesWorked = []       
        window.Element('-QSO-').update(QSOCount)
        window.Element('-Counties-').update(countyScore)
        window.Element('-Score-').update(score)    
        # erase the contents of the scores file
        with open('scores.csv', 'w') as scores:
            scores.truncate(0)
#***********************************
# get the stored log to display in the table
def displayContacts():
    try:
        df = pd.read_csv('log.csv')  
        data = df.values.tolist()        
        return data           
    except IOError:        
        fileCreate = sg.popup_ok('File not found, click OK to create')
        if fileCreate == 'OK':
            with open('log.csv', 'w') as logfile:
                   logwriter = csv.writer(logfile)
                   logwriter.writerow(['Call', 'Time', 'RST', 'Mode', 'County or Serial#'])
                   data = logwriter.values.tolist()               
#************************************

counties = ['Annapolis', 'Antigonish', 'Cape Breton', 'Colchester', 'Cumberland', 
            'Digby', 'Guysborough','Halifax', 'Hants', 'Inverness', 'Kings', 'Lunenburg', 
            'Pictou', 'Queens', 'Richmond', 'Shelburne', 'Victoria', 'Yarmouth']
modes = ['Phone', 'CW', 'Digital']
headings = ['Call', 'Time', 'RaST', 'Mode', 'County or Serial#']

# ------ Menu Definition ------ #
menu_def = [['&File', ['&Setup', ['Your Callsign', 'Contest Date', ], '&Clear Scores', 'E&xit']],
            ['&Edit', ['&Paste', ['Special', 'Normal', ], 'Undo'], ],            
            ['&Help', '&About...'] 
           ]
# ------------------------------#

layout =[
        [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
        [sg.Frame(layout = [[sg.T('Call:'), sg.I(size = (10, 1), k = '-Call-'), sg.T('Time:'), sg.I(default_text = current_time, size = (10, 1), k = '-Time-'), sg.T('RST:'),
        sg.I(size = (10, 1), default_text = '59', k = '-RST-'), sg.T('Mode:'), sg.Combo(values = (modes), default_value = 'Phone', size = (10, 1), k = '-Mode-'), sg.T('County or Serial:'), sg.Combo(values = counties, size = (15,1), k = '-County-')],
        [sg.B('Save', tooltip = 'Save this QSO to the log', focus = True, size = (15,1), bind_return_key = True, pad = ((80, 0),(20,20))), sg.B('Clear', tooltip = 'Clear all fields', size = (15,1), pad = (80, 0)), sg.B('Exit', tooltip = 'Exit the logger', size = (15, 1), pad = (80, 1))]],title = "Input", pad = ((20, 20),(20, 20)))],
        [sg.Frame(layout = [[sg.T("QSO's: "), sg.T(QSOCount, size = (5, 1), k = '-QSO-'), sg.T("Counties: "), sg.T(len(countiesWorked), size = (5, 1),k = '-Counties-'), sg.T("Score: "), sg.T(score, size = (5, 1),k = '-Score-')]], title = 'Score', pad = ((20, 20),(0, 20))), sg.T(callSign, size = (10, 1),k = '-Callsign-'), sg.T(contest_date, size = (20, 1), k = '-Contest_Date-')],        
        [sg.Table(values = displayContacts(), headings=headings, max_col_width=25,            
            auto_size_columns=False,
            display_row_numbers=True,
            justification='center',
            def_col_width = 15,
            num_rows=10,
            alternating_row_color='lightyellow',
            key='-Table-',
            row_height=35,
            tooltip='Displays your current log.')],
          [sg.Button('Change Colors')],          
          [sg.Text('Change Colors = Changes the colors of rows 8 and 9')],
        ] 
        
window = sg.Window('NSARA Contest Logger', 
                    layout, font = 'Arial', 
                    element_justification = 'l', 
                    grab_anywhere = True, resizable = True) 
 
while True:
    event, values = window.read() 
                                                                                          
    if event == 'Exit' or event == sg.WIN_CLOSED:          
        #Write the scores to a local file for next session      
        with open('scores.csv', 'w') as scores:
            scores.write(str(QSOCount) + ',')           
            scores.write(str(score) + '\n')            
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
        call_sign = sg.popup_get_text('Enter your Callsign or SWL for shortwave listener', title = 'Your Callsign')
        with open('call.csv', 'w') as call:
            call_writer = csv.writer(call)
            call_writer.writerow([call_sign])       
        # This will display the callsign as soon as OK is clicked in the popup.
        window['-Callsign-'].Update(call_sign.upper())

    if event == 'Contest Date':
        get_contest_date = sg.popup_get_date(title = 'Choose the Contest Date', no_titlebar = False)        
        contest_date = datetime.datetime.strptime(str(get_contest_date),'(%m, %d, %Y)').strftime('%B %d, %Y')
        with open('date.csv', 'w') as date:
            date_writer = csv.writer(date)
            date_writer.writerow([contest_date])        
        # This will display the contest date as soon as OK is clicked in the popup.
        window['-Contest_Date-'].Update(contest_date.upper())      

    if event == 'Clear Scores':        
        clearScores()   
    #**************
    # when the save button is pressed
    if event == 'Save':     
        # make sure that the call and county fields have a value in them
        if values['-Call-'] != '' and values['-County-'] != '': 
            #******************
            # build a list of the calls that have been worked
            if not values['-Call-'] in callList:
                callList.append(values['-Call-'])               
            #*****************  
             # build a list of the values entered
                logentry = []
                logentry.append(values['-Call-'])
                logentry.append(current_time)
                logentry.append(values['-RST-'])
                logentry.append(values['-Mode-'])
                logentry.append(values['-County-'])
                #***************************************
                # append each log entry to the .csv file (Apr 18)
                with open('log.csv', 'a+') as logfile:
                   logwriter = csv.writer(logfile)
                   logwriter.writerow(logentry)
                #***************************************              

                # Display the refreshed table after each entry
                window['-Table-'].Update(values=displayContacts()) 
                                                                                                                            
            #****************
            # Display a runing total of QSO's, new counties worked and total score.
            QSOCount+=1            
            window.Element('-QSO-').update(QSOCount)
            if not values['-County-'] in countiesWorked and values['-County-'] in counties:
                countiesWorked.append(values['-County-']) 
                # append each new county to counties.txt (Jun 1)
                with open('counties.txt', 'a') as logfile:                  
                   logfile.write("{}".format((values['-County-'])))
                   logfile.write("\n")                
                #***************************************
            countyScore = len(countiesWorked)              
            window.Element('-Counties-').update(countyScore)
            # if the first log entry is a serial number not a county(avoid multiply by zero error)
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