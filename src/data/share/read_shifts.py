import ast

from src.data.share.utils.check_service_date_validity import (
    checkServiceDateValidity
    )
from src.data.share.utils.get_service_date import getServiceDate
from src.data.share.color_manager import (getPrimaryColor,
                                          getShiftColor,
                                          getFreeDayColor,
                                          getErrorColor)

def readShifts(offNum):
    filePath = 'data/data/all_shifts_by_driver_decrypted/' + offNum + '.txt'
    weekServices = ''

    try:
        fileR = open(filePath, 'r', encoding='utf-8')
        weekServices = fileR.readlines()
        fileR.close()
    except:
        return None
    
    weekServicesData = []
    currWeekService = 0
    while(currWeekService < len(weekServices)):
        weekService = ast.literal_eval(weekServices[currWeekService])
        if(not checkServiceDateValidity(weekService)):
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
            bgColor2 = getFreeDayColor()
            if(weekService[1] == 'empty' or
               weekService[1] == '' or # za svaki slucaj case-vi
               weekService[1] == ' '):
                bgColor2 = getErrorColor()
                
            weekServicesData.append({'firstItem': weekService[0],
                                     'firstDriver': '',
                                     'secondItem': '\n'.join(weekService[1:]),
                                     'secondDriver': '',
                                     'bg_color1': getPrimaryColor(),
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
            elif(firstDriver.count('-') > 2):
                firstDriver = firstDriver.replace('-', ' - ', 1)
                
            secondDriver = secondShift[-1]
            if(secondDriver == 'empty'): 
                secondShift = [0]
                secondDriver = ''
            elif('ANON' in secondDriver):
                secondDriver = ''
            elif(secondDriver.count('-') > 2):
                secondDriver = secondDriver.replace('-', ' - ', 1)
                
            thirdDriver = thirdShift[-1]
            if(thirdDriver == 'empty'): 
                thirdShift = [0]
                thirdDriver = ''
            elif('ANON' in thirdDriver):
                thirdDriver = ''
            elif(thirdDriver.count('-') > 2):
                thirdDriver = thirdDriver.replace('-', ' - ', 1)

            weekServicesData.append({'firstItem': weekService[0],
                                     'firstDriver': '',
                                     'secondItem': '\n'.join(firstShift[:-1]),
                                     'secondDriver': firstDriver,
                                     'bg_color1': getPrimaryColor(),
                                     'bg_color2': getShiftColor()})
            weekServicesData.append({'firstItem': '\n'.join(secondShift[:-1]),
                                     'firstDriver': secondDriver,
                                     'secondItem': '\n'.join(thirdShift[:-1]),
                                     'secondDriver': thirdDriver,
                                     'bg_color1': getShiftColor(),
                                     'bg_color2': getShiftColor()})
            currWeekService = currWeekService + 3
    return weekServicesData
