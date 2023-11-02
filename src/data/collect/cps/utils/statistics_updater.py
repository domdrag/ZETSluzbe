from decimal import Decimal

from src.data.manager.statistics_manager import (
    getEmptyStatisticsMonthDict,
    getMonthDict,
    setStatistics,
    initializeStatisticsDict
    )

STATISTICS = initializeStatisticsDict()

# using float sometimes results in very small decimal numbers (24.560000002 instead of 24.56)
# saving str instead of float (Decimal not accepted to JSON) because of the same issue
def addNumbers(number1, number2):
    return str(Decimal(number1) + Decimal(number2))

def updateStatistics(offNum, month, hourlyRateStats, driveOrder, receptionPoint, releasePoint):
    monthDict = getMonthDict(STATISTICS, offNum, month)

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


def updateStatisticsVac(offNum, month, vacationType, isHolidayOnWorkDay):
    monthDict = getMonthDict(STATISTICS, offNum, month)
    hourlyRateDict = monthDict['SATNICA']
    if (vacationType not in hourlyRateDict):
        hourlyRateDict[vacationType] = 0
    hourlyRateDict[vacationType] = hourlyRateDict[vacationType] + 1

    if (vacationType == 'I-GO' or vacationType == 'I-BO' or isHolidayOnWorkDay):
        hourlyRateDict['UKUPNO'] = addNumbers(hourlyRateDict['UKUPNO'], 8)

def finishStatisticsUpdate():
    setStatistics(STATISTICS)