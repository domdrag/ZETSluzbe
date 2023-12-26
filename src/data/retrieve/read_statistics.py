from src.data.manager.statistics_manager import StatisticsManager
from src.data.manager.monthly_hours_fund_manager import getMonthlyHoursFund

HOURLY_RATE_SORTED_KEYS = ['ODRADENO', 'NOCNA', 'DRUGA', 'SUBOTA', 'NEDJELJA', 'O', 'UKUPNO']

def fixKey(key):
    return (key.replace('_', ' ')).capitalize()

def appendStatisticData(statisticsData, dictionary, title, editKeys = False):
    statisticContentData = []
    for key,value in dictionary.items():
        if (editKeys):
            fixedKey = fixKey(key)
        else:
            fixedKey = key
        statisticContentData.append({'statisticContentItem': fixedKey,
                                     'statisticContentValue': str(value),
                                     'neighboursCount': len(dictionary)})

    statisticsData.append({'statisticTitle': title,
                           'statisticContentData': statisticContentData})

def orderDict(dictionary, isHourlyRateDict = False):
    # if I recall, python keeps the order of dict initialization
    if (isHourlyRateDict):
        hourlyRateKeys = list(dictionary.keys())
        leftovers = list(set(hourlyRateKeys) - set(HOURLY_RATE_SORTED_KEYS))
        if (leftovers):
            keyOrder = HOURLY_RATE_SORTED_KEYS[:-1] + leftovers + [HOURLY_RATE_SORTED_KEYS[-1]]
        else:
            keyOrder = HOURLY_RATE_SORTED_KEYS
        return {key: dictionary[key] for key in keyOrder if key in dictionary}
    else:
        return dict(sorted(dictionary.items()))

def readStatistics(offNum, monthFormat):
    monthDict = StatisticsManager.getDriverMonthStatistics(offNum, monthFormat)
    monthlyHoursFundDict = getMonthlyHoursFund(monthFormat)
    statisticsData = []

    appendStatisticData(statisticsData,
                        orderDict(monthlyHoursFundDict),
                        'MJESECNI FOND SATI',
                        editKeys = True)
    appendStatisticData(statisticsData,
                        orderDict(monthDict['SATNICA'], isHourlyRateDict = True),
                        'SATNICA',
                        editKeys = True)
    appendStatisticData(statisticsData, orderDict(monthDict['LINIJE']), 'LINIJE')
    appendStatisticData(statisticsData, orderDict(monthDict['MJESTA_PRIMANJA']), 'MJESTA PRIMANJA')
    appendStatisticData(statisticsData, orderDict(monthDict['MJESTA_PUSTANJA']), 'MJESTA PUSTANJA')
    return statisticsData

