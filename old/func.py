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

def isLegitOffNum(x):
    if(not x.isdigit()):
        return False
    x = int(x)
    if(x>=1000 and x<=99999):
        return True
    if(x>3720304 and x<400000):
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

def getDriverOffNumber(serviceNumber, day):
    print(serviceNumber, day, 'HELO')
    firstURL = 'https://www.zet.hr/interno/UserDocsImages/tp%20dubrava/Slu%C5%BEbe%20za%20sve%20voza%C4%8De/tpd.pdf'

    PDFFile = download_file(firstURL)
    PDF = pdfplumber.open(PDFFile)
    found = False
    for pageNum in range(len(PDF.pages)):
        print('PAGEN', pageNum)
        page = PDF.pages[pageNum]
        textFirstPDF = page.extract_text()
        listFirstPDF = re.split(' |\n', textFirstPDF)
        nextElementGenerator = (i for i,v in enumerate(listFirstPDF) if v == serviceNumber)
        foundIndex = next(nextElementGenerator, -1)
        while(foundIndex != -1):
            index = foundIndex - day - 1
            if(index < 0):
                foundIndex = next(nextElementGenerator, -1)
                continue
            
            wantedOffNum = listFirstPDF[index]
            print(serviceNumber, wantedOffNum)
            if(isLegitOffNum(wantedOffNum)):
                print(1, wantedOffNum)
                found = True
                break
            
            foundIndex = next(nextElementGenerator, -1)
        if(found):
            print(2, wantedOffNum)
            break
    print(3, wantedOffNum)
    if(not found):
        return -1
    else:
        return wantedOffNum[1:]

def getDriverInfo(offNum):
    if(offNum == -1):
        return ['ANON']
    #print(offNum)
    fileR = open('vozaci.txt', 'r', encoding='utf-8')
    lines = fileR.readlines()
    fileR.close()

    found = False
    for line in lines:
        driverInfo = re.split(' ', line)
        if(driverInfo[0] == offNum):
            found = True
            break
        
    if(not found):
        return ['ANON'] 

    driverInfo.pop(0)
    driverInfo.pop(0)
    driverInfo[1] = driverInfo[1][:-1]
    driverInfo.pop(2)
    return driverInfo
    
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
                
                
def readServices(offNumFile, fridayFlag, fullServices):
    offNum = offNumFile[:4]
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

    #workDayURL = getWorkDayURL()
    #saturdayURL = getSaturdayURL()
    #sundayURL = getSundayURL()

    workDayURL = 'https://www.zet.hr/interno/UserDocsImages/TP%20Raspored%20rada/Oglasne%20plo%C4%8De%20RD_internet%20od%2011.7.22..pdf'
    saturdayURL = 'https://www.zet.hr/interno/UserDocsImages/TP%20Raspored%20rada/Oglasne%20plo%C4%8De%20SUB_internet%20od%2016.7.22..pdf'
    sundayURL = 'https://www.zet.hr/interno/UserDocsImages/TP%20Raspored%20rada/Oglasne%20plo%C4%8De%20NED_internet%20od%2026.6.22..pdf'

    services = []

    for i in range(0, len(serviceNumbers), 1):
        if(serviceNumbers[i] == 'O' or serviceNumbers[i] == 'O\n'):
            fileW = open(offNumFile, 'a', encoding='utf-8')            
            fileW.write(f"{[days[i], 'O']}\n")
            fileW.close()
            services.append([days[i], 'O'])
            continue
        
        if(days[i] in holidays2022):
            URL = sundayURL
        elif(i == 5):
            URL = saturdayURL
        elif(i == 6):
            URL = sundayURL
        else:
            URL = workDayURL

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

        if(fullServices):
            numOfServices = 3
        else:
            numOfServices = 1

        for serviceStartIndex in [0,8,15]:
            if(serviceStartIndex == 8 and numOfServices == 1):
                break
            # prva sluzba index 0
            # druga sluzba index 8
            # treca sluzba index 15
            print(serviceLine)
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
            serviceLayout.append(releaseTime + ', ' + releasePoint + ', ')
            if(numOfServices == 3):
                driverOffNumber = getDriverOffNumber(serviceNumber, i)
                driverInfo = getDriverInfo(driverOffNumber)
                driverInfo = ' '.join(driverInfo)
                serviceLayout.append(driverInfo)
            print(serviceLayout)

            # ako je petak i imamo subotu nedjelju tada ne radi
            # nista ako nisu izasle odnosno ucitaj ako su izasle
            currentWeekDay = datetime.datetime.today().weekday()
            if(i == 0 and currentWeekDay == 4 and fridayFlag == True):
                fileR = open(offNumFile, 'r', encoding='utf-8')
                lines = fileR.readlines()
                fileR.close()
                lastRecordedSundayService = ast.literal_eval(lines[len(lines)-1])

                lastRecordedSundayDate = getServiceDate(lastRecordedSundayService)
                pageMondayDate = getServiceDate(serviceLayout)
                daysDiff = (pageMondayDate - lastRecordedSundayDate).days
                if(daysDiff < 0):
                    return []

            fileW = open(offNumFile, 'a', encoding='utf-8')
            fileW.write(f"{serviceLayout}\n")
            fileW.close()
            
            services.append(serviceLayout)
            
    return services

def getRequiredDaysDiff(offNumFile):
    fileR = open(offNumFile, 'r', encoding='utf-8')
    lines = fileR.readlines()
    fileR.close()
    
    lastRecordedSundayService = ast.literal_eval(lines[len(lines)-1])
    lastRecordedSundayDate = getServiceDate(lastRecordedSundayService)

    todayDate = getTodayDate()
    dateDiff = todayDate - lastRecordedSundayDate
    return dateDiff.days

def checkAndDeleteServices(offNumFile):
    fileR = open(offNumFile, 'r', encoding='utf-8')
    lines = fileR.readlines()
    fileR.close()

    if(len(lines) <= 11):
        return
    
    fileW = open(offNumFile, 'w', encoding='utf-8')
    for i in range(len(lines)):
        if(len(lines) - i > 11):
            pass
        else:
            fileW.write(lines[i])
    fileW.close()

def servicesRun(offNum, fullServices):
    loadServices = False
    fridayFlag = False
    offNumFile = offNum
    if(fullServices):
        offNumFile = offNumFile + 'FULL.txt'
    else:
        offNumFile = offNum + '.txt'

    if(not os.path.exists(offNumFile)):
        loadServices = True

    else:
        # razlika danasnjeg datuma i zadnje recordane Nedjelje
        daysDiff = getRequiredDaysDiff(offNumFile) 

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
    if(loadServices == True and os.path.exists(offNumFile)):
        fileR = open(offNumFile, 'r', encoding='utf-8')
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
                
        servicesTemp = services + readServices(offNumFile, fridayFlag, fullServices)
        services = []
        for service in servicesTemp:
            serviceDate = getServiceDate(service)
            todayDate = getTodayDate()
            daysDiff = (serviceDate - todayDate).days
            if(daysDiff >= -1):  
                services.append(service)
        
        checkAndDeleteServices(offNumFile)
        
    elif(loadServices == True):
        fileW = open(offNumFile, 'w', encoding='utf-8').close()
        servicesTemp = readServices(offNumFile, fridayFlag, fullServices)
        services = []
        for service in servicesTemp:
            serviceDate = getServiceDate(service)
            todayDate = getTodayDate()
            daysDiff = (serviceDate - todayDate).days
            if(daysDiff >= -1):  
                services.append(service)

    else:
        fileR = open(offNumFile, 'r', encoding='utf-8')
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


