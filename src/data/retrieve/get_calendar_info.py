import ast

from src.data.manager.design_manager import DesignManager

def getCalendarInfo(offNum):
    filePath = 'data/data/all_services_by_driver_decrypted/' + offNum + '.txt'
    weekServices = ''
    
    try:
        fileR = open(filePath, 'r', encoding='utf-8')
        weekServices = fileR.readlines()
        fileR.close()
    except:
        return []
    
    calendarInfoData = []
    for weekServiceRawString in weekServices:
        weekService = ast.literal_eval(weekServiceRawString)
        fullDay = weekService[0]
        commaIndex = fullDay.index(',')
        dayName = fullDay[0:commaIndex]
        date = fullDay[commaIndex+2:]
        firstDotIndex = date.index('.')
        secondDotIndex = date.index('.', firstDotIndex+1)
        thirdDotIndex = date.index('.', secondDotIndex+1)
        day = int(date[:firstDotIndex])
        month = int(date[firstDotIndex+1:secondDotIndex])
        year = int(date[secondDotIndex+1:thirdDotIndex])
                
        if(len(weekService) == 2):
            dayColor = DesignManager.getFreeDayColor()
            if(weekService[1] == 'empty' or
               weekService[1] == '' or # za svaki slucaj case-vi
               weekService[1] == ' '):
                dayColor = DesignManager.getPrimaryColor()
            calendarInfoData.append({'day': day,
                                     'month': month,
                                     'year': year,
                                     'dayColor': dayColor,
                                     'serviceFullDay': weekService[0],
                                     'service': '\n'.join(weekService[1:])})
        else:
            calendarInfoData.append({'day': day,
                                     'month': month,
                                     'year': year,
                                     'dayColor': DesignManager.getServiceColor(),
                                     'serviceFullDay': weekService[0],
                                     'service': '\n'.join(weekService[1:])})
    return calendarInfoData

