import os
import requests
import pdfplumber
import re
import os.path
import ast
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta, FR
from bs4 import BeautifulSoup, SoupStrainer

# cannot change (hopefully)
firstURL = 'https://www.zet.hr/interno/UserDocsImages/tp%20dubrava/Slu%C5%BEbe%20za%20sve%20voza%C4%8De/tpd.pdf'
# can change
workDayURL = ''
saturdayURL = ''
sundayURL = ''
mondayDate = date(2022,1,1)


def download_file(url):
    local_filename = url.split('/')[-1]
    
    with requests.get(url) as r:
        assert r.status_code == 200, f'error, status code is {r.status_code}'
        with open(local_filename, 'wb') as f:
            f.write(r.content)
        
    return local_filename

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

def isMoreThanThreeDigit(x):
    if(not x.isdigit()):
        return False
    x = int(x)
    if(x >= 999):
        return True
    return False

def getStringDate(date):
    return str(date.day) + '.' + str(date.month) + '.' + str(date.year) + '.'

def deleteExceeded(directory):
    files = os.listdir('./' + directory)
    if(directory == 'services'):
        maxExceed = 7
    else:
        maxExceed = 21
    
    for file in files:
        if(file == 'keep.txt'): # gitHub ne dozvoljava prazan folder
            continue
        fileName = './' + directory + '/' + file
        fileR = open(fileName, 'r', encoding='utf-8')
        lines = fileR.readlines()
        fileR.close()

        if(len(lines) <= maxExceed):
            return

        fileW = open(fileName, 'w', encoding='utf-8')
        for i in range(len(lines)):
            if(len(lines) - i > maxExceed):
                pass
            else:
                fileW.write(lines[i])
        fileW.close()
        
def deleteAllFiles():
    files = os.listdir(os.curdir)
    for file in files:
        if file.endswith(".pdf"):
            os.remove(file)
            
    files = os.listdir('./relevant')
    for file in files:
        if(file == 'vozaci.txt'):
            continue
        if(file == 'lastRecordDate.txt'):
            continue
        os.remove(os.path.join('./relevant', file))

    deleteExceeded('services')
    deleteExceeded('shifts')

    '''files = os.listdir('./services')
    for file in files:
        os.remove(os.path.join('./services', file))

    files = os.listdir('./shifts')
    for file in files:
        os.remove(os.path.join('./shifts', file))'''

def searchLinks():
    global workDayURL
    global saturdayURL
    global sundayURL

    payload = {
        'pojam': 'zetovci'
    }

    with requests.Session() as s:
        p = s.post('https://www.zet.hr/interno/default.aspx?a=login', data=payload)
        r = s.get('https://www.zet.hr/interno/default.aspx?id=1041')
        content = r.content

        for link in BeautifulSoup(content, parse_only=SoupStrainer('a')):
            if hasattr(link, "href"):
                link = link['href']
                if('RD' in link):
                    workDayURL = link
                if('SUB' in link):
                    saturdayURL = link
                if('NED' in link):
                    sundayURL = link

def setLastRecord():
    global mondayDate
    fileW = open('relevant/lastRecordDate.txt', 'w', encoding='utf-8')
    fileW.write(f"{[mondayDate.year, mondayDate.month, mondayDate.day]}\n")
    fileW.close()

def getDays(days, textFirstPDF):
    odIndex = textFirstPDF.find('od')
    stringForMonth = textFirstPDF[odIndex:odIndex+50]
    stringForMonthList = re.split(' |\.', stringForMonth)
    day = stringForMonthList[1]
    month = stringForMonthList[2]
    year = stringForMonthList[3]

    global mondayDate
    mondayDate = date(int(year), int(month), int(day))
    mondayDate + datetime.timedelta(days = 1)

    try:
        fileR = open('relevant/lastRecordDate.txt', 'r', encoding='utf-8')
        line = fileR.readline()
        fileR.close()
        lastRecordDateList = ast.literal_eval(line)
        lastRecordedDate = date(lastRecordDateList[0],
                                lastRecordDateList[1],
                                lastRecordDateList[2])
    except:
        lastRecordedDate = date(2022, 9, 4) #nedjelja pa sigurno nisu isti
    if(mondayDate == lastRecordedDate):
        return False

    monday = 'Ponedjeljak, ' + getStringDate(mondayDate)
    nextDate = mondayDate + datetime.timedelta(days = 1)
    tuesday = 'Utorak, ' + getStringDate(nextDate)
    nextDate = nextDate + datetime.timedelta(days = 1)
    wednesday = 'Srijeda, ' + getStringDate(nextDate)
    nextDate = nextDate + datetime.timedelta(days = 1)
    thursday = 'Cetvrtak, ' + getStringDate(nextDate)
    nextDate = nextDate + datetime.timedelta(days = 1)
    friday = 'Petak, ' + getStringDate(nextDate)
    nextDate = nextDate + datetime.timedelta(days = 1)
    saturday = 'Subota, ' + getStringDate(nextDate)
    nextDate = nextDate + datetime.timedelta(days = 1)
    sunday = 'Nedjelja, ' + getStringDate(nextDate)

    days.append(monday)
    days.append(tuesday)
    days.append(wednesday)
    days.append(thursday)
    days.append(friday)
    days.append(saturday)
    days.append(sunday)
    return True

def setDays(days):
    holidays2022 = ['15.8.','1.12.','18.11.','25.12.','26.12.']
    PDFFile = download_file(firstURL)
    with pdfplumber.open(PDFFile) as PDF:
        page = PDF.pages[0]
        textFirstPDF = page.extract_text()
    return getDays(days, textFirstPDF)
    
def readWeekServices():
    holidays2022 = ['15.8.','1.12.','18.11.','25.12.','26.12.']

    PDFFile = download_file(firstURL)
    with pdfplumber.open(PDFFile) as PDF:
 
        # citamo sluzbe za ovaj tjedan
        fileW = open('relevant/services.txt', 'w', encoding='utf-8')
        for page in PDF.pages:
            tables = page.dedupe_chars().find_tables()
            for tableId in tables:
                table = tableId.extract()
                for services in table:
                    if(isinstance(services[0], str) and services[0].isnumeric()):
                        if(not services[0]):
                            continue
                        fileW.write(f"{services[0:8]}\n")
                        if(not services[8]):
                            continue
                        fileW.write(f"{services[8:]}\n")
        fileW.close()
    return 1

#### pomogao jsvine
def readService(typeOfDay, URL):
    PDFFile = download_file(URL)

    with pdfplumber.open(PDFFile) as PDF:
        fileW = open('relevant/' + typeOfDay + '.txt', 'w', encoding='utf-8')
        for page in PDF.pages:
            filtered = (page.filter(lambda obj: not (obj.get("non_stroking_color") == (0, 0, 1) and obj.get("width", 100) < 100)).dedupe_chars())
            tables = filtered.extract_tables()
            for table in tables:
                for serviceLine in table:
                    if(isinstance(serviceLine[0], str) and serviceLine[0].isnumeric()):
                        fileW.write(f"{serviceLine}\n")
    fileW.close()
####

def readAllServices():
    readService('workDay', workDayURL)
    readService('saturday', saturdayURL)
    readService('sunday', sundayURL)
    

def getServiceLine(serviceNum, day):
    if(not serviceNum.isnumeric()):
        return [serviceNum]
    if(day < 5):
        fileR = open('relevant/workDay.txt', 'r', encoding='utf-8')
    elif(day == 5):
        fileR = open('relevant/saturday.txt', 'r', encoding='utf-8')
    else:
        fileR = open('relevant/sunday.txt', 'r', encoding='utf-8')
    serviceLines = fileR.readlines()
    fileR.close()
    for serviceLine in serviceLines:
        serviceLine = ast.literal_eval(serviceLine)
        if(serviceNum in serviceLine):
            return serviceLine
    return []


def getServiceLayout(serviceLine, serviceNum, days, day):
    if(len(serviceLine) == 1):
        return [days[day], serviceLine[0]]
    serviceLayout = []
    serviceStartIndex = 0
    if(not serviceNum.isnumeric()):
        serviceLayout.append(days[day])
        serviceLayout.append(serviceNum)
        return [days[day], 'empty']
    if(serviceLine == []):
        return [days[day], 'empty']
    if(any(x is None for x in serviceLine)):
        return [days[day], 'empty']
    if(serviceLine[8] == serviceNum):
        serviceStartIndex = 8
    if(serviceLine[15] == serviceNum):
        serviceStartIndex = 15
    if(serviceLine[serviceStartIndex+2] == ''):
        return [days[day], 'empty']
    
    serviceNumber = serviceLine[serviceStartIndex]
    driveOrder = serviceLine[serviceStartIndex+1]
    receptionPoint = serviceLine[serviceStartIndex+2].replace('\n','')
    receptionTime = serviceLine[serviceStartIndex+3]
    releaseTime = serviceLine[serviceStartIndex+4]

    if('\n' in receptionTime): # dvokratne
        startingTimes = re.split('\n| ', receptionTime)
        startingTimes = list(filter(('').__ne__, startingTimes))
        if(len(startingTimes[0]) == 1):
            startingTimes[0] = startingTimes[0] + startingTimes[1]
            del startingTimes[1]
        receptionTime = startingTimes[0] + ', ' + startingTimes[1]

        startingTimes = re.split('\n| ', releaseTime)
        startingTimes = list(filter(('').__ne__, startingTimes))
        if(len(startingTimes[0]) == 1):
            startingTimes[0] = startingTimes[0] + startingTimes[1]
            del startingTimes[1]
        releaseTime = startingTimes[0] + ', ' + startingTimes[1]
        
        startingPlaces = re.split(' ', receptionPoint)
        startingPlaces = list(filter(('').__ne__, startingPlaces))
        receptionPoint = startingPlaces[0]
        releasePoint = startingPlaces[1]

    elif(driveOrder == ''): # pricuva
        driveOrder = 'PRIČUVA'
        releasePoint = receptionPoint
        
    else:
        releasePoint = 'PTD/PTT'
        for element in serviceLine[serviceStartIndex+3:]:
            if(isAlphaWithSpaces(element)):
                releasePoint = element.replace('\n','')
    
            
    # slaganje za layout
    serviceLayout = []
    serviceLayout.append(days[day])
    serviceLayout.append('broj sluzbe: ' + serviceNumber)
    serviceLayout.append('vozni red: ' + driveOrder)
    serviceLayout.append(receptionTime + ', ' + receptionPoint)
    serviceLayout.append(releaseTime + ', ' + releasePoint)
    return serviceLayout
    

def writeServices(days):
    fileR = open('relevant/services.txt', 'r', encoding='utf-8')
    weekServicesALL = fileR.readlines()
    fileR.close()
    for weekServicesRaw in weekServicesALL:
        weekServices = ast.literal_eval(weekServicesRaw)
        offNum = int(weekServices[0])
        fileW = open('services/' + str(offNum) + '.txt', 'a', encoding='utf-8')
        for i in range(1,8):
            serviceNum = weekServices[i]
            serviceLine = getServiceLine(serviceNum, i-1)
            serviceLayout = getServiceLayout(serviceLine, serviceNum, days, i-1)
            fileW.write(f"{serviceLayout}\n")
        fileW.close()

def getDriverInfo(serviceNum, driverList, day):
    fileR = open('relevant/services.txt', 'r', encoding='utf-8')
    weekServicesALL = fileR.readlines()
    fileR.close()
    wantedOffNum = -1
    for weekServicesRaw in weekServicesALL:
        weekServices = ast.literal_eval(weekServicesRaw)
        if(weekServices[day] == serviceNum):
            wantedOffNum = int(weekServices[0])
            break
        
    if(wantedOffNum == -1):
        return ['ANON', 'XXX-XXX-XXXX']

    for driver in driverList:
        if(driver[0] == str(wantedOffNum)):
            driverName = driver[1] + ' ' + driver[2][:-1]
            telNum = driver[3]
            driverTelNumber = f"{telNum[:3]}-{telNum[3:6]}-{telNum[6:]}"
            return [driverName, driverTelNumber]
    return ['ANON', 'XXX-XXX-XXXX']

def writeShifts(days):
    fileR = open('relevant/services.txt', 'r', encoding='utf-8')
    weekServicesALL = fileR.readlines()
    fileR.close()

    fileR = open('relevant/vozaci.txt', 'r', encoding='utf-8')
    driversRaw = fileR.readlines()
    fileR.close()
    driverList = []
    for driverRaw in driversRaw:
        driver = driverRaw.split()
        driverList.append(driver)
        
    for weekServicesRaw in weekServicesALL:
        weekServices = ast.literal_eval(weekServicesRaw)
        offNum = int(weekServices[0])
        fileW = open('shifts/' + str(offNum) + '.txt', 'a', encoding='utf-8')        
        for i in range(1,8):
            serviceNum = weekServices[i]
            serviceLine = getServiceLine(serviceNum, i-1)
            if(len(serviceLine) == 1):
                serviceLayout = getServiceLayout(serviceLine, serviceNum, days, i-1)
                fileW.write(f"{serviceLayout}\n")
                continue
            if(serviceLine == []):
                fileW.write(f"{[days[i-1], 'UNABLE TO FIND SERVICE LINE']}\n")
                continue
            for j in [0,8,15]:
                wantedServiceNum = serviceLine[j]
                serviceLayout = getServiceLayout(serviceLine, wantedServiceNum, days, i-1)
                if(serviceLayout[1] == 'empty'):
                    fileW.write(f"{serviceLayout}\n")
                    continue
                driverInfo = getDriverInfo(wantedServiceNum, driverList, i)
                serviceLayout.append(driverInfo[0] + '\n' + driverInfo[1])
                fileW.write(f"{serviceLayout}\n")
        fileW.close()
            
def updateBefore(updateCheck):
    days = []

    try:
        searchLinks()
        print('LINKS FOUND')
        
        if(updateCheck and not setDays(days)):
            return 0
        print('DAYS SET')

        deleteAllFiles()
        print('DELETED ALL FILES')
        
        readWeekServices()
        print('READ WEEK SERVICES DONE')
        
        readAllServices()
        print('READ ALL SERVICES DONE')
        
        writeServices(days)
        print('WRITE WEEK SERVICES DONE')
        
        writeShifts(days)
        print('WRITE WEEK SHIFTS DONE')

        setLastRecord()
        print('LAST RECORD SET')
        return 1
    except:
        return 2

globalDays = []

def update(updateLevel):
    global globalDays
    try:
        if(updateLevel == 0):
            searchLinks()
            print('LINKS FOUND')
            return 'Postavljanje datuma'
        elif(updateLevel == 1):
            if(not setDays(globalDays)):
                return '0'
            print('DAYS SET')
            return 'Brisanje starih dokumenata'

        elif(updateLevel == 2):           
            deleteAllFiles()
            print('DELETED ALL FILES')
            return 'Citanje tjednih sluzbi'

        elif(updateLevel == 3):
            readWeekServices()
            print('READ WEEK SERVICES DONE')
            return 'Citanje svih sluzbi'

        elif(updateLevel == 4):
            readAllServices()
            print('READ ALL SERVICES DONE')
            return 'Zapisivanje tjednih sluzbi'
        
        elif(updateLevel == 5):
            writeServices(globalDays)
            print('WRITE WEEK SERVICES DONE')
            return 'Zapisivanje tjednih smjena'
        
        elif(updateLevel == 6):
            writeShifts(globalDays)
            print('WRITE WEEK SHIFTS DONE')
            return 'Postavljanje datuma zadnjeg azuriranja'

        elif(updateLevel == 7):
            setLastRecord()
            print('LAST RECORD SET')
            return 'Kopiranje sluzbi'
        elif(updateLevel == 8):
            return '1'
    except:
        return '2'

