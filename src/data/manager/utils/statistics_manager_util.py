from decimal import Decimal

def getEmptyStatisticsMonthDict():
    return {'SATNICA': {'ODRADENO': '0',
                        'NOCNA': '0',
                        'DRUGA': '0',
                        'SUBOTA': '0',
                        'NEDJELJA': '0',
                        'UKUPNO': '0'},
            'LINIJE': {},
            'MJESTA_PRIMANJA': {},
            'MJESTA_PUSTANJA': {}}

def getMonthDict(statistics, offNum, month):
    if (offNum not in statistics):
        statistics[offNum] = dict()
    offNumDict = statistics[offNum]
    if (month not in offNumDict):
        offNumDict[month] = getEmptyStatisticsMonthDict()
    return offNumDict[month]

def addNumbers(number1, number2):
    return str(Decimal(number1) + Decimal(number2))

def updateStatisticsImpl(monthDict, hourlyRateStats, driveOrder, receptionPoint, releasePoint):
    serviceDuration = hourlyRateStats['serviceDuration']
    nightHours = hourlyRateStats['nightHours']
    secondShift = hourlyRateStats['secondShift']
    isSaturday = hourlyRateStats['isSaturday']
    isSunday = hourlyRateStats['isSunday']

    hourlyRateDict = monthDict['SATNICA']
    hourlyRateDict['ODRADENO'] = addNumbers(hourlyRateDict['ODRADENO'], serviceDuration)
    hourlyRateDict['NOCNA'] = addNumbers(hourlyRateDict['NOCNA'], nightHours)
    hourlyRateDict['DRUGA'] = addNumbers(hourlyRateDict['DRUGA'], secondShift)
    if (isSaturday):
        hourlyRateDict['SUBOTA'] = addNumbers(hourlyRateDict['SUBOTA'], serviceDuration)
    if (isSunday):
        hourlyRateDict['NEDJELJA'] = addNumbers(hourlyRateDict['NEDJELJA'], serviceDuration)
    hourlyRateDict['UKUPNO'] = addNumbers(hourlyRateDict['UKUPNO'], serviceDuration)

    lineNumbersDict = monthDict['LINIJE']
    lineNumber = (driveOrder.split('.'))[0]
    if (lineNumber not in lineNumbersDict):
        lineNumbersDict[lineNumber] = 0
    lineNumbersDict[lineNumber] = lineNumbersDict[lineNumber] + 1

    receptionPointsDict = monthDict['MJESTA_PRIMANJA']
    if (receptionPoint not in receptionPointsDict):
        receptionPointsDict[receptionPoint] = 0
    receptionPointsDict[receptionPoint] = receptionPointsDict[receptionPoint] + 1

    releasePointsDict = monthDict['MJESTA_PUSTANJA']
    if (releasePoint not in releasePointsDict):
        releasePointsDict[releasePoint] = 0
    releasePointsDict[releasePoint] = releasePointsDict[releasePoint] + 1