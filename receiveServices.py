import ast
import re
import os
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta, FR

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

def getTodayDate():
    now = datetime.datetime.now()
    todayDate = date(now.year, now.month, now.day)
    return todayDate

def checkService(weekService):
    todayDate = getTodayDate()
    serviceDate = getServiceDate(weekService)
    dateDiff = serviceDate - todayDate
    if(dateDiff.days >= 0):
        return True
    else:
        return False

def receiveServices(offNum):
    filePath = 'services/' + offNum + '.txt'
    if(not os.path.exists(filePath)):
        return []
    
    fileR = open(filePath, 'r', encoding='utf-8')
    weekServices = fileR.readlines()
    fileR.close()
    weekServicesData = []
    for weekServiceRawString in weekServices:
        weekService = ast.literal_eval(weekServiceRawString)
        if(not checkService(weekService)):
           continue
        if(len(weekService) == 2):
            bgColor = (0.13, 0.55, 0.13, 1)
            if(weekService[1] == 'empty' or
               weekService[1] == '' or # za svaki slucaj case-vi
               weekService[1] == ' '):
                bgColor = (0.545, 0, 0, 1)
            weekServicesData.append({'day': weekService[0],
                                     'service': '\n'.join(weekService[1:]),
                                     'bg_color': bgColor})
        else:
            weekServicesData.append({'day': weekService[0],
                                     'service': '\n'.join(weekService[1:]),
                                     'bg_color': (0, 0, 1, 1)})
    return weekServicesData

def receiveShifts(offNum):
    fileR = open('shifts/' + offNum + '.txt', 'r', encoding='utf-8')
    weekServices = fileR.readlines()
    fileR.close()
    weekServicesData = []
    currWeekService = 0
    while(currWeekService < len(weekServices)):
        weekService = ast.literal_eval(weekServices[currWeekService])
        if(not checkService(weekService)):
            currWeekService = currWeekService + 1
            continue
        currServiceDate = getServiceDate(weekService)
        if(currWeekService + 1 == len(weekServices)):
            previousService = ast.literal_eval(weekServices[currWeekService - 1]) #dummy
            nextServiceDate = getServiceDate(previousService) #dummy
        else:
            nextService = ast.literal_eval(weekServices[currWeekService + 1])
            nextServiceDate = getServiceDate(nextService)
        if(currServiceDate != nextServiceDate): # slobodan dan
            bgColor2 = (0.13, 0.55, 0.13, 1)
            if(weekService[1] == 'empty' or
               weekService[1] == '' or # za svaki slucaj case-vi
               weekService[1] == ' '):
                bgColor2 = (0.545, 0, 0, 1)
                
            weekServicesData.append({'firstItem': weekService[0],
                                     'firstDriver': '',
                                     'secondItem': '\n'.join(weekService[1:]),
                                     'secondDriver': '',
                                     'bg_color1': (0,0,0,0),
                                     'bg_color2': bgColor2})
            currWeekService = currWeekService + 1
        else:
            firstShift = ast.literal_eval(weekServices[currWeekService])[1:]
            secondShift = ast.literal_eval(weekServices[currWeekService + 1])[1:]
            thirdShift = ast.literal_eval(weekServices[currWeekService+ 2])[1:]

            firstDriver = firstShift[-1]
            if(firstDriver == 'empty'): 
                firstShift = [0]
                firstDriver = ''
            elif('ANON' in firstDriver):
                firstDriver = ''
                
            secondDriver = secondShift[-1]
            if(secondDriver == 'empty'): 
                secondShift = [0]
                secondDriver = ''
            elif('ANON' in secondDriver):
                secondDriver = ''
                
            thirdDriver = thirdShift[-1]
            if(thirdDriver == 'empty'): 
                thirdShift = [0]
                thirdDriver = ''
            elif('ANON' in thirdDriver):
                thirdDriver = ''
            
            weekServicesData.append({'firstItem': weekService[0],
                                     'firstDriver': '\n \n',
                                     'secondItem': '\n'.join(firstShift[:-1]),
                                     'secondDriver': firstDriver,
                                     'bg_color1': (0,0,0,0),
                                     'bg_color2': (1, 0.6, 0, 1)})
            weekServicesData.append({'firstItem': '\n'.join(secondShift[:-1]),
                                     'firstDriver': secondDriver,
                                     'secondItem': '\n'.join(thirdShift[:-1]),
                                     'secondDriver': thirdDriver,
                                     'bg_color1': (1, 0.6, 0, 1),
                                     'bg_color2': (1, 0.6, 0, 1)})
            currWeekService = currWeekService + 3
    return weekServicesData

