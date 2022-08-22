### ISSUES ###
# 2) linkovi - sredjeni zasad. Nemozes spremat linkove jer ih vjerojatno ne micu | probati ubrzati check_file?
# 3) os metode; checking first then opening file might be problematic
## https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions
# 4) prebaciti spremanje u services u funkciju
# 5) upis offNuma, smjene ..

import os
import requests
import pdfplumber
import re
import os.path
import ast
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta, FR

def check_file(url):
    r = requests.head(url)
    return r.status_code == 200
    
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
    # ovo bi trebao biti stalan link
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

def getTodayDate():
    now = datetime.datetime.now()
    todayDate = date(now.year, now.month, now.day)
    return todayDate

def getServiceDate(service):
    serviceDate = (re.split(' ', service[0]))[1]
    firstDot = serviceDate.index('.')
    secondDot = firstDot+1 + serviceDate[firstDot+1:].index('.')
    thirdDot = secondDot+1 + serviceDate[secondDot+1:].index('.')
    day = int(serviceDate[0:firstDot])
    month = int(serviceDate[firstDot+1:secondDot])
    year = int(serviceDate[secondDot+1:thirdDot])
    serviceRealDate = date(year, month, day)
    return serviceRealDate

def getWorkDayURL():
    now = datetime.datetime.now()
    thisYear = str(now.year)[-2:]
    thisMonth = str(now.month)
    common = 'https://www.zet.hr/interno/UserDocsImages/TP%20Raspored%20rada/Oglasne%20plo%C4%8De%20RD_internet%20od%20'
    for month in range(int(thisMonth), 0, -1):
        for day in range(31, 0, -1):
            print(day, month)
            url = common + str(day) + '.'
            url = url + str(month) + '.'
            url = url + thisYear + '..pdf'

            if(check_file(url)):
                return url

def getSaturdayURL():
    now = datetime.datetime.now()
    thisYear = str(now.year)[-2:]
    thisMonth = str(now.month)
    common = 'https://www.zet.hr/interno/UserDocsImages/TP%20Raspored%20rada/Oglasne%20plo%C4%8De%20SUB_internet%20od%20'
    for month in range(int(thisMonth), 0, -1):
        for day in range(31, 0, -1):
            print(day, month)
            url = common + str(day) + '.'
            url = url + str(month) + '.'
            url = url + thisYear + '..pdf'
            
            if(check_file(url)):
                return url

def getSundayURL():
    now = datetime.datetime.now()
    thisYear = str(now.year)[-2:]
    thisMonth = str(now.month)
    common = 'https://www.zet.hr/interno/UserDocsImages/TP%20Raspored%20rada/Oglasne%20plo%C4%8De%20NED_internet%20od%20'
    for month in range(int(thisMonth), 0, -1):
        for day in range(31, 0, -1):
            print(day, month)
            url = common + str(day) + '.'
            url = url + str(month) + '.'
            url = url + thisYear + '..pdf'

            if(check_file(url)):
                return url
                    
                
                
def readServices(offNum, fridayFlag):
    holidays2022 = ['15.8.','1.12.','18.11.','25.12.','26.12.']
    
    servicesData = getServiceNumbers(offNum)
    textFirstPDF = servicesData[0]
    indexOffNum = servicesData[1]

    odIndex = textFirstPDF.find('od')
    stringForMonth = textFirstPDF[odIndex:odIndex+50]
    stringForMonthList = re.split(' |\.', stringForMonth)
    month = stringForMonthList[2]
    year = stringForMonthList[3]

    radnikIndex = textFirstPDF.find('Radnik')
    stringForDates = textFirstPDF[radnikIndex:radnikIndex+100]
    stringForDatesList = re.split(' |\n', stringForDates)
 
    monday = 'Ponedjeljak, ' + stringForDatesList[2] + '.' + month + '.' + year + '.'
    tuesday = 'Utorak, ' + stringForDatesList[3] + '.' + month + '.' + year + '.'
    wednesday = 'Srijeda, ' + stringForDatesList[4] + '.' + month + '.' + year + '.'
    thursday = 'Cetvrtak, ' + stringForDatesList[5] + '.' + month + '.' + year + '.'
    friday = 'Petak, ' + stringForDatesList[6] + '.' + month + '.' + year + '.'
    saturday = 'Subota, ' + stringForDatesList[7] + '.' + month + '.' + year + '.'
    sunday = 'Nedjelja, ' + stringForDatesList[8] + '.' + month + '.' + year + '.'

    days = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]

    textCutLeft = textFirstPDF[indexOffNum:]
    listCutLeft = re.split(' |\n', textCutLeft)
    nextOffNumGenerator = (i for i,v in enumerate(listCutLeft) if isFourDigit(v))
    tempThrow = next(nextOffNumGenerator)
    nextOffNum = next(nextOffNumGenerator)
    serviceNumbers = listCutLeft[1:nextOffNum]

    '''checkURLs = False
    if(os.path.exists('workingLinks.txt')):
        fileR = open('workingLinks.txt', 'r', encoding='utf-8')
        lines = fileR.read().splitlines()
        fileR.close()

        if(len(lines) != 3):
            pass
        else:
            workDayURL = lines[0]
            saturdayURL = lines[1]
            sundayURL = lines[2]

            if(not check_file(workDayURL)):
                checkURLs = False
            elif(not check_file(saturdayURL)):
                checkURLs = False
            elif(not check_file(sundayURL)):
                checkURLs = False
            else:
                checkURLs = True'''

    #if(not checkURLs):
    #fileW = open('workingLinks.txt', 'w', encoding='utf-8').close()
    workDayURL = getWorkDayURL()
    saturdayURL = getSaturdayURL()
    sundayURL = getSundayURL()
        
    #workDayURL = 'https://www.zet.hr/interno/UserDocsImages/TP%20Raspored%20rada/Oglasne%20plo%C4%8De%20RD_internet%20od%2011.7.22..pdf'
    #saturdayURL = 'https://www.zet.hr/interno/UserDocsImages/TP%20Raspored%20rada/Oglasne%20plo%C4%8De%20SUB_internet%20od%2016.7.22..pdf'
    #sundayURL = 'https://www.zet.hr/interno/UserDocsImages/TP%20Raspored%20rada/Oglasne%20plo%C4%8De%20NED_internet%20od%2026.6.22..pdf'

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

        # ako je petak i imamo subotu nedjelju tada ne radi nista ako nisu izasle odnosno ucitaj ako su izasle
        currentWeekDay = datetime.datetime.today().weekday()
        if(i == 0 and currentWeekDay == 4 and fridayFlag == True):
            fileR = open(offNum + '.txt', 'r', encoding='utf-8')
            lines = fileR.readlines()
            fileR.close()
            lastRecordedSundayService = ast.literal_eval(lines[len(lines)-1])

            lastRecordedSundayDate = getServiceDate(lastRecordedSundayService)
            pageMondayDate = getServiceDate(serviceLayout)
            daysDiff = (pageMondayDate - lastRecordedSundayDate).days
            if(daysDiff < 0):
                return []

        fileW = open(offNum + '.txt', 'a', encoding='utf-8')
        fileW.write(f"{serviceLayout}\n")
        fileW.close()
        
        services.append(serviceLayout)
    return services

def getRequiredDaysDiff(offNum):
    fileR = open(offNum + '.txt', 'r', encoding='utf-8')
    lines = fileR.readlines()
    fileR.close()
    
    lastRecordedSundayService = ast.literal_eval(lines[len(lines)-1])
    lastRecordedSundayDate = getServiceDate(lastRecordedSundayService)

    todayDate = getTodayDate()
    dateDiff = todayDate - lastRecordedSundayDate
    return dateDiff.days

def checkAndDeleteServices(offNum):
    fileR = open(offNum + '.txt', 'r', encoding='utf-8')
    lines = fileR.readlines()
    fileR.close()

    if(len(lines) <= 11):
        return
    
    fileW = open(offNum + '.txt', 'w', encoding='utf-8')
    for i in range(len(lines)):
        if(len(lines) - i > 11):
            pass
        else:
            fileW.write(lines[i])
    fileW.close()

def servicesRun(offNum):
    loadServices = False
    fridayFlag = False

    if(not os.path.exists(offNum + '.txt')):
        loadServices = True

    else:
        # razlika danasnjeg datuma i zadnje recordane Nedjelje
        daysDiff = getRequiredDaysDiff(offNum) 

    currentWeekDay = datetime.datetime.today().weekday()

    if(loadServices == True):
        pass

    elif(currentWeekDay == 0):
        if(daysDiff >= 1):
            loadServices = True

    elif(currentWeekDay == 1):
        if(daysDiff >= 2):
            loadServices = True
            
    elif(currentWeekDay == 2):
        if(daysDiff >= 3):
            loadServices = True
            
    elif(currentWeekDay == 3):
        if(daysDiff >= 4):
            loadServices = True
        
    elif(currentWeekDay == 4):
        if(daysDiff >= -2):
            loadServices = True
            if(daysDiff == -2):
                fridayFlag = True
            
    elif(currentWeekDay == 5):
        if(daysDiff >= -1):
            loadServices = True
            
    else:
        if(daysDiff >= 0):
            loadServices = True
            

    services = []
    if(loadServices == True and os.path.exists(offNum + '.txt')):
        fileR = open(offNum + '.txt', 'r', encoding='utf-8')
        lines = fileR.readlines()
        fileR.close()

        for line in lines:
            service = ast.literal_eval(line)
            if(len(services) > 0):
                services.append(service)
                continue
            
            serviceDate = getServiceDate(service)
            todayDate = getTodayDate()
            daysDiff = (serviceDate - todayDate).days
            if(daysDiff >= -1): # samo ponedjeljak, petak, subota ili nedjelja (ako zadovoljavaju) (algoritam.txt)
                services.append(service)
                
        servicesTemp = services + readServices(offNum, fridayFlag)
        services = []
        for service in servicesTemp:
            serviceDate = getServiceDate(service)
            todayDate = getTodayDate()
            daysDiff = (serviceDate - todayDate).days
            if(daysDiff >= -1):  
                services.append(service)
        
        checkAndDeleteServices(offNum)
        
    elif(loadServices == True):
        fileW = open(offNum + '.txt', 'w', encoding='utf-8').close()
        servicesTemp = readServices(offNum, fridayFlag)
        services = []
        for service in servicesTemp:
            serviceDate = getServiceDate(service)
            todayDate = getTodayDate()
            daysDiff = (serviceDate - todayDate).days
            if(daysDiff >= -1):  
                services.append(service)

    else:
        fileR = open(offNum + '.txt', 'r', encoding='utf-8')
        lines = fileR.readlines()
        fileR.close()

        for line in lines:
            service = ast.literal_eval(line)
            if(len(services) > 0):
                services.append(service)
                continue
            
            serviceDate = getServiceDate(service)
            todayDate = getTodayDate()
            daysDiff = (serviceDate - todayDate).days
            if(daysDiff >= -1):
                services.append(service)
    return services
    

###################################################


