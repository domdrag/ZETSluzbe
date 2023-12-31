import ast

from src.data.retrieve.utils.get_services import getServices
from src.data.manager.design_manager import DesignManager

def getCalendarInfo(offNum):
    weekServices = ''
    try:
        weekServices = getServices(offNum)
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

