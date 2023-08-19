import json

from src.data.share.config_manager import getConfig
from src.data.share.utils.get_monthly_hours_fund import getMonthlyHoursFund

HOURLY_RATE_SORTED_KEYS = ['ODRADENO', 'NOCNA', 'DRUGA', 'SUBOTA', 'NEDJELJA', 'O', 'UKUPNO']

def getEmptyMonthDict():
    return {'SATNICA': {'ODRADENO': '0',
                        'NOCNA': '0',
                        'DRUGA': '0',
                        'SUBOTA': '0',
                        'NEDJELJA': '0',
                        'UKUPNO': '0'},
            'LINIJE': {},
            'MJESTA_PRIMANJA': {},
            'MJESTA_PUSTANJA': {}}

def getStatistics(offNum, month):
    with open('data/data/statistics.json', 'r', encoding='utf-8') as statisticsFile:
        STATISTICS = json.load(statisticsFile)

    if (offNum not in STATISTICS):
        return getEmptyMonthDict()
    offNumDict = STATISTICS[offNum]
    if (month not in offNumDict):
        return getEmptyMonthDict()
    return offNumDict[month]

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

def readStatistics(offNum):
    config = getConfig()
    lastRecordDate = config['LAST_RECORD_DATE']
    year = lastRecordDate[0]
    month = lastRecordDate[1]
    monthFormat = str(month) + '-' + str(year)
    monthDict = getStatistics(offNum, monthFormat)
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

