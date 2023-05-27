import ast

from src.data.share.utils.get_holidays import getHolidays

COLOR_BLUE = (0, 0, 1, 1)
COLOR_GREEN = (0.13, 0.55, 0.13, 1)
COLOR_RED = (0.13, 0.55, 0.13, 1)
COLOR_GREY = (0.5, 0.5, 0.5, 1)

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
        holidays = getHolidays()
        isHoliday = False
        
        for holiday in holidays:
            if (year == holiday[0] and
                month == holiday[1] and
                day == holiday[2]):
                isHoliday = True
                
        if(len(weekService) == 2):
            dayColor = COLOR_GREEN
            if(weekService[1] == 'empty' or
               weekService[1] == '' or # za svaki slucaj case-vi
               weekService[1] == ' '):
                dayColor = COLOR_GREY
            calendarInfoData.append({'day': day,
                                     'month': month,
                                     'year': year,
                                     'dayColor': dayColor,
                                     'isHoliday': isHoliday,
                                     'service': '\n'.join(weekService[1:])})
        else:
            calendarInfoData.append({'day': day,
                                     'month': month,
                                     'year': year,
                                     'dayColor': COLOR_BLUE,
                                     'isHoliday': isHoliday,
                                     'service': '\n'.join(weekService[1:])})
    return calendarInfoData

