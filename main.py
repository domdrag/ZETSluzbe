### ISSUES ###
# 2) linkovi
# 3) os metode; checking first then opening file might be problematic
## https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions

import os
import requests
import pdfplumber
import re
import os.path
import ast
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta, FR

def download_file(url):
    local_filename = url.split('/')[-1]
    
    with requests.get(url) as r:
        assert r.status_code == 200, f'error, status code is {r.status_code}'
        with open(local_filename, 'wb') as f:
            f.write(r.content)
        
    return local_filename

def isFourDigit(x):
    if(not x.isdigit()):
        return False
    x = int(x)
    if(x>=1000 and x<=9999):
        return True
    return False

def isTwoOrThreeDigit(x):
    if(not x.isdigit()):
        return False
    x = int(x)
    if(x>=10 and x<=999):
        return True
    return False

def isAlphaWithSpaces(x):
    if(x == ''):
        return False
    y = re.split('\n|\.| ',x)
    for el in y:
        if(el == ''):
            continue
        if(not el.isalpha()):
            return False
    return True

def getServiceNumbers(offNum):
    firstURL = 'https://www.zet.hr/interno/UserDocsImages/tp%20dubrava/Slu%C5%BEbe%20za%20sve%20voza%C4%8De/tpd.pdf'

    PDFFile = download_file(firstURL)
    PDF = pdfplumber.open(PDFFile)
    for pageNum in range(len(PDF.pages)):
        page = PDF.pages[pageNum]
        textFirstPDF = page.extract_text()
        indexOffNum = textFirstPDF.find(offNum)
        if(indexOffNum != -1):
            break

    return [textFirstPDF, indexOffNum]

def readServices(offNum):
    holidays2022 = ['15.8.','1.12.','18.11.','25.12.','26.12.']
    
    servicesData = getServiceNumbers(offNum)
    textFirstPDF = servicesData[0]
    indexOffNum = servicesData[1]

    odIndex = textFirstPDF.find('od')
    stringForMonth = textFirstPDF[odIndex:odIndex+40]
    stringForMonthList = re.split(' |\.', stringForMonth)
    month = stringForMonthList[2]

    radnikIndex = textFirstPDF.find('Radnik')
    stringForDates = textFirstPDF[radnikIndex:radnikIndex+100]
    stringForDatesList = re.split(' |\n', stringForDates)
 
    monday = 'Ponedjeljak, ' + stringForDatesList[2] + '.' + month + '.'
    tuesday = 'Utorak, ' + stringForDatesList[3] + '.' + month + '.'
    wednesday = 'Srijeda, ' + stringForDatesList[4] + '.' + month + '.'
    thursday = 'Cetvrtak, ' + stringForDatesList[5] + '.' + month + '.'
    friday = 'Petak, ' + stringForDatesList[6] + '.' + month + '.'
    saturday = 'Subota, ' + stringForDatesList[7] + '.' + month + '.'
    sunday = 'Nedjelja, ' + stringForDatesList[8] + '.' + month + '.'

    days = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]

    textCutLeft = textFirstPDF[indexOffNum:]
    listCutLeft = re.split(' |\n', textCutLeft)
    nextOffNumGenerator = (i for i,v in enumerate(listCutLeft) if isFourDigit(v))
    tempThrow = next(nextOffNumGenerator)
    nextOffNum = next(nextOffNumGenerator)
    serviceNumbers = listCutLeft[1:nextOffNum]

    workDayURL = 'https://www.zet.hr/interno/UserDocsImages/TP%20Raspored%20rada/Oglasne%20plo%C4%8De%20RD_internet%20od%2011.7.22..pdf'
    saturdayURL = 'https://www.zet.hr/interno/UserDocsImages/TP%20Raspored%20rada/Oglasne%20plo%C4%8De%20SUB_internet%20od%2016.7.22..pdf'
    sundayURL = 'https://www.zet.hr/interno/UserDocsImages/TP%20Raspored%20rada/Oglasne%20plo%C4%8De%20NED_internet%20od%2026.6.22..pdf'

    services = []

    for i in range(0, len(serviceNumbers), 1):
        if(serviceNumbers[i] == 'O' or serviceNumbers[i] == 'O\n'):
            fileW = open(offNum + '.txt', 'a', encoding='utf-8')
            fileW.write(f"{[days[i], 'O']}\n")
            fileW.close()
            services.append([days[i], 'O'])
            continue
        
        if(days[i] in holidays2022):
            URL = sundayURL
            fileStart = 'sundayPage'
        elif(i == 5):
            URL = saturdayURL
            fileStart = 'saturdayPage'
        elif(i == 6):
            URL = sundayURL
            fileStart = 'sundayPage'
        else:
            URL = workDayURL
            fileStart = 'workDayPage'

        PDFFile = download_file(URL)
        PDF = pdfplumber.open(PDFFile)
        for page in PDF.pages:
            mTextSecondPDF = page.extract_text()
            mStart = mTextSecondPDF.find(serviceNumbers[i])
            if(mStart != -1):
                break

        tables = page.find_tables()
        found = False
        for tableId in tables:
            table = tableId.extract()
            for serviceLine in table:
                if(serviceNumbers[i] in serviceLine):
                    found = True
                    break
            if(found):
                break
            
        serviceStartIndex = serviceLine.index(serviceNumbers[i])
        serviceNumber = serviceLine[serviceStartIndex]
        driveOrder = serviceLine[serviceStartIndex+1]
        receptionPoint = serviceLine[serviceStartIndex+2].replace('\n','')
        receptionTime = serviceLine[serviceStartIndex+3]
        
        if(receptionPoint == 'PTD' or receptionPoint == 'PTT'):
            driveOrder = 'PRIČUVA'
            releasePoint = receptionPoint
        else:
            releasePoint = 'PTD'
            for element in serviceLine[serviceStartIndex+3:]:
                if(isAlphaWithSpaces(element)):
                    releasePoint = element.replace('\n','')
                
        releaseTime = serviceLine[serviceStartIndex+4]
            
        
        # slaganje za layout
        serviceLayout = []
        serviceLayout.append(days[i])
        serviceLayout.append('broj sluzbe: ' + serviceNumber)
        serviceLayout.append('vozni red: ' + driveOrder)
        serviceLayout.append(receptionTime + ', ' + receptionPoint)
        serviceLayout.append(releaseTime + ', ' + releasePoint)

        fileW = open(offNum + '.txt', 'a', encoding='utf-8')
        fileW.write(f"{serviceLayout}\n")
        fileW.close()
        
        services.append(serviceLayout)
    return services

###################################################
# Pitaj medu za url-ove

offNum = '2621'
now = datetime.datetime.now()
currentTime = now.time()
currentWeekDay = datetime.datetime.today().weekday()

lastFriday = datetime.datetime.now() + relativedelta(weekday=FR(-1))
lastFridayFileName = str(lastFriday.day) + '.' + str(lastFriday.month) + '.txt'

if(not os.path.exists(offNum + '.txt')):
    # brisemo sve .txt fileove
    allFiles = os.listdir(os.curdir)
    for file in allFiles:
        if file.endswith('.txt'):
            os.remove(file)

elif(not os.path.exists(lastFridayFileName)):

    fileR = open(offNum + '.txt', 'r', encoding='utf-8')
    lines = fileR.readlines()
    fileR.close()
    lastRecordedFridayService = ast.literal_eval(lines[len(lines)-3])
    lastRecordedFridayDate = (re.split(' ', lastRecordedFridayService[0]))[1]
    firstDot = lastRecordedFridayDate.index('.')
    secondDot = firstDot+1 + lastRecordedFridayDate[firstDot+1:].index('.')
    lastRecordedFridayDay = int(lastRecordedFridayDate[0:firstDot])
    lastRecordedFridayMonth = int(lastRecordedFridayDate[firstDot+1:secondDot])
    lastRecordedFridayDate = date(now.year, lastRecordedFridayMonth, lastRecordedFridayDay)
    todayDate = date(now.year, now.month, now.day)

    daysDiff = todayDate - lastRecordedFridayDate
    daysDiff = abs(daysDiff)
    if(daysDiff.days < 7):
        # ostavi petak,subota,nedjelja
        fileRW = open(offNum + '.txt', 'r+', encoding='utf-8')
        lines = fileRW.readlines()
        fileRW.seek(0)
        print(len(lines))
        for i in range(len(lines)):
            if(i >= len(lines) - 3):
                fileRW.write(lines[i])
            else:
                pass
        fileRW.truncate()
        fileRW.close()
        
    
    elif(daysDiff.days == 7 and currentTime.hour < 12): #petak
        # izbaci sluzbe (bit ce ili prosli ili dobar tjedan zavisno jesu li izasle)
        open(offNum + '.txt', 'w', encoding='utf-8').close()
        pass
    
    else:
        # izbrisi sve
        fileW = open(offNum + '.txt', 'w', encoding='utf-8').close()
        

services = []
if(os.path.exists(lastFridayFileName) and os.path.exists(offNum + '.txt')):
    fileR = open(offNum + '.txt', 'r', encoding='utf-8')
    lines = fileR.readlines()
    fileR.close()

    for line in lines:
        service = ast.literal_eval(line)
        services.append(service)

else:
    if(os.path.exists(offNum + '.txt')):
        fileR = open(offNum + '.txt', 'r', encoding='utf-8')
        lines = fileR.readlines()
        fileR.close()

        for line in lines:
            service = ast.literal_eval(line)
            services.append(service)
    
    services = services + readServices(offNum)
    fileW = open(lastFridayFileName, 'w', encoding='utf-8').close()



from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

#kv codes
Builder.load_string('''
<Sluzbe>:
    id: main_win
    RecycleView:
        viewclass: 'CustomLabel'
        id: table_floor
        RecycleGridLayout:
            id: table_floor_layout
            cols: 5
            default_size: (None,250)
            default_size_hint: (1,None)
            size_hint_y: None
            height: self.minimum_height
            spacing: 5
<CustomLabel@Label>:
    bcolor: (1,1,1,1)
    canvas.before:
        Color:
            rgba: root.bcolor
        Rectangle:
            size: root.size
            pos: self.pos
''')

class Sluzbe(BoxLayout):
    def __init__(self,table='', **kwargs):
        super().__init__(**kwargs)

        table_data = []
        for i in range(len(services)):    
            if(services[i][1] == 'O'):
                table_data.append({'text':services[i][0],'size_hint_y':None,
                                   'height':100,'bcolor':(.05,.30,.80,1),
                                   'halign':'center', 'valign':'top'}) #append the data
                table_data.append({'text':'\n'.join(services[i][1:]),'size_hint_y':None,
                                   'height':300,'bcolor':(.10,.50,.150,1),
                                   'halign':'center', 'valign':'top'}) #append the data 
                
            else:
                table_data.append({'text':services[i][0],'size_hint_y':None,
                                   'height':100,'bcolor':(.05,.30,.80,1),
                                   'halign':'center', 'valign':'top'}) #append the data
                table_data.append({'text':'\n'.join(services[i][1:]),'size_hint_y':None,
                                   'height':300,'bcolor':(.06,.25,.50,1),
                                   'halign':'center', 'valign':'top'}) #append the data 

        self.ids.table_floor_layout.cols = 1 #define value of cols to the value of self.columns
        self.ids.table_floor.data = table_data #add table_data to data value

class SluzbeApp(App):
    def build(self):
        return Sluzbe()

if __name__=='__main__':
    SluzbeApp().run()

