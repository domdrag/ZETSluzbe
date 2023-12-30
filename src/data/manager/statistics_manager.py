import json
import copy

from src.data.manager.utils.statistics_manager_util import *

STATISTICS_FILE_PATH = 'data/central_data/statistics.json'

class StatisticsManager:
    __currentStatistics__ = dict()
    __updatedStatistics__ = dict()

    @staticmethod
    def load():
        with open(STATISTICS_FILE_PATH, 'r', encoding='utf-8') as statisticsFile:
            StatisticsManager.__currentStatistics__ = json.load(statisticsFile)
        StatisticsManager.__updatedStatistics__ = copy.deepcopy(StatisticsManager.__currentStatistics__)

    @staticmethod
    def getDriverStatistics(offNum):
        currentStatistics = StatisticsManager.__currentStatistics__
        if (offNum not in currentStatistics):
            return getEmptyStatisticsMonthDict()
        return currentStatistics[offNum]

    @staticmethod
    def getDriverMonthStatistics(offNum, month):
        currentStatistics = StatisticsManager.__currentStatistics__
        if (offNum not in currentStatistics):
            return getEmptyStatisticsMonthDict()
        offNumDict = currentStatistics[offNum]
        if (month not in offNumDict):
            return getEmptyStatisticsMonthDict()
        return offNumDict[month]

    @staticmethod
    def finishUpdate():
        updatedStatistics = StatisticsManager.__updatedStatistics__
        with open(STATISTICS_FILE_PATH, 'w', encoding='utf-8') as statisticsFile:
            json.dump(updatedStatistics, statisticsFile, indent=3)

    @staticmethod
    def updateStatistics(offNum, month, hourlyRateStats, driveOrder, receptionPoint, releasePoint):
        updatedStatistics = StatisticsManager.__updatedStatistics__
        monthDict = getMonthDict(updatedStatistics, offNum, month)
        updateStatisticsImpl(monthDict, hourlyRateStats, driveOrder, receptionPoint, releasePoint)

    @staticmethod
    def updateStatisticsVac(offNum, month, vacationType, isHolidayOnWorkDay):
        updatedStatistics = StatisticsManager.__updatedStatistics__
        monthDict = getMonthDict(updatedStatistics, offNum, month)
        hourlyRateDict = monthDict['SATNICA']
        if (vacationType not in hourlyRateDict):
            hourlyRateDict[vacationType] = 0
        hourlyRateDict[vacationType] = hourlyRateDict[vacationType] + 1

        if (vacationType == 'I-GO' or vacationType == 'I-BO' or isHolidayOnWorkDay):
            hourlyRateDict['UKUPNO'] = addNumbers(hourlyRateDict['UKUPNO'], 8)
