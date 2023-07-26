import re
from decimal import Decimal

from src.data.admin.utils.statistics_manager import updateStatistics, updateStatisticsVac
from src.data.share.get_holidays import getHolidays

def isAlphaWithSpaces(x):
    if(x == ''):
        return False
    y = re.split('\n|\.| |-',x)
    for el in y:
        if(el == ''):
            continue
        if(not el.isalpha()):
            return False
    return True

def getServiceLayout(serviceLine, serviceNum, days, day, offNum = None):
    if(len(serviceLine) == 1):
        if serviceLine[0] == '' or serviceLine[0] == ' ':
            return [days[day], 'empty']
        if (offNum):
            dayInfoList = days[day].split(',')
            dateList = dayInfoList[1].split('.')
            monthFormat = dateList[1] + '-' + dateList[2]

            dateListInt = [int(dateList[0]), int(dateList[1]), int(dateList[2])]
            holidays = getHolidays()
            isHoliday = False
            for holiday in holidays:
                holiday = holiday[::-1]
                if ((holiday == dateListInt) or
                    (holiday[2] == 0 and holiday[:2] == dateListInt[:2])):
                    isHoliday = True
                    break

            updateStatisticsVac(offNum,
                                monthFormat,
                                serviceLine[0],
                                isHoliday)
        return [days[day], serviceLine[0]]

    nightHoursPossible = True
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
        nightHoursPossible = False
        serviceStartIndex = 8
    if(serviceLine[15] == serviceNum):
        serviceStartIndex = 15
    if(serviceLine[serviceStartIndex+2] == ''):
        return [days[day], 'empty']
    
    serviceNumber = serviceLine[serviceStartIndex]
    driveOrder = serviceLine[serviceStartIndex+1]
    receptionPoint = serviceLine[serviceStartIndex+2].replace('\n',' ')
    receptionPoint = re.sub(' +', ' ', receptionPoint)  
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
                releasePoint = element.replace('\n',' ')
                releasePoint = re.sub(' +', ' ', releasePoint) 
                break

    if (offNum):
        serviceDuration = serviceLine[serviceStartIndex + 5]
        if (nightHoursPossible):
            nightHours = serviceLine[serviceStartIndex + 6]
            secondShift = serviceLine[serviceStartIndex + 7]
        else:
            nightHours = ''
            secondShift = serviceLine[serviceStartIndex + 6]

        serviceDurationFloat = Decimal(serviceDuration.replace(',', '.'))
        if (nightHours):
            nightHoursFloat = Decimal(nightHours.replace(',', '.'))
        else:
            nightHoursFloat = 0
        if (secondShift):
            secondShiftFloat = Decimal(secondShift.replace(',', '.'))
        else:
            secondShiftFloat = 0

        dayInfoList = days[day].split('.')
        monthFormat = dayInfoList[-3] + '-' + dayInfoList[-2]
        isSaturday = (day == 5)
        isSunday = (day == 6)
        hourlyRateStats = {'serviceDuration': serviceDurationFloat,
                           'nightHours': nightHoursFloat,
                           'secondShift': secondShiftFloat,
                           'isSaturday': isSaturday,
                           'isSunday': isSunday}

        updateStatistics(offNum, monthFormat, hourlyRateStats, driveOrder, receptionPoint, releasePoint)
    
            
    # slaganje za layout
    serviceLayout = []
    serviceLayout.append(days[day])
    serviceLayout.append('broj sluzbe: ' + serviceNumber)
    serviceLayout.append('vozni red: ' + driveOrder)
    serviceLayout.append(receptionTime + ', ' + receptionPoint)
    serviceLayout.append(releaseTime + ', ' + releasePoint)
    return serviceLayout
    
def getServiceLayoutAndUpdateStats(serviceLine, serviceNum, days, day, offNum):
    return getServiceLayout(serviceLine, serviceNum, days, day, offNum)