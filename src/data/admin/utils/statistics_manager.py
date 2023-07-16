import json
from decimal import Decimal

STATISTICS = dict()

def getEmptyMonthDict():
    return {'ODRADENO': '0',
            'NOCNA': '0',
            'DRUGA': '0',
            'SUBOTA': '0',
            'NEDJELJA': '0',
            'DRUGA': '0',
            'I-GO': 0,
            'I-BO': 0,
            'O': 0,
            'Og': 0,
            'Oz': 0,
            'Ob': 0,
            'UKUPNO': '0'}

def getMonthDict(offNum, month):
    global STATISTICS
    if (not STATISTICS):
        with open('data/data/statistics.json', 'r') as statisticsFile:
            STATISTICS = json.load(statisticsFile)

    if (offNum not in STATISTICS):
        STATISTICS[offNum] = dict()
    offNumDict = STATISTICS[offNum]
    if (month not in offNumDict):
        offNumDict[month] = getEmptyMonthDict()
    return offNumDict[month]

# using float sometimes results in very small decimal numbers (24.560000002 instead of 24.56)
# saving str instead of float (Decimal not accepted to JSON) because of the same issue
def addNumbers(number1, number2):
    return str(Decimal(number1) + Decimal(number2))
def updateStatistics(offNum, month, serviceDuration, nightHours, secondShift, isSaturday, isSunday):
    monthDict = getMonthDict(offNum, month)
    monthDict['ODRADENO'] = addNumbers(monthDict['ODRADENO'], serviceDuration)
    monthDict['NOCNA'] = addNumbers(monthDict['NOCNA'], nightHours)
    monthDict['DRUGA'] = addNumbers(monthDict['DRUGA'], secondShift)
    if (isSaturday):
        monthDict['SUBOTA'] = addNumbers(monthDict['SUBOTA'], serviceDuration)
    if (isSunday):
        monthDict['NEDJELJA'] = addNumbers(monthDict['NEDJELJA'], serviceDuration)
    monthDict['UKUPNO'] = addNumbers(monthDict['UKUPNO'], serviceDuration)

def updateStatisticsVac(offNum, month, vacationType, isHoliday):
    monthDict = getMonthDict(offNum, month)
    if (vacationType not in monthDict):
        monthDict[vacationType] = 0
    monthDict[vacationType] = monthDict[vacationType] + 1

    if (vacationType == 'I-GO' or vacationType == 'I-BO' or isHoliday):
        monthDict['UKUPNO'] = addNumbers(monthDict['UKUPNO'], 8)

def setStatistics():
    with open('data/data/statistics.json', 'w') as statisticsFile:
        json.dump(STATISTICS, statisticsFile, indent = 3)
