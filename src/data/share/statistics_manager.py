import json
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

def getDriverStatistics(offNum):
    with open('data/data/statistics.json', 'r', encoding='utf-8') as statisticsFile:
        STATISTICS = json.load(statisticsFile)

    if (offNum not in STATISTICS):
        return getEmptyStatisticsMonthDict()
    return STATISTICS[offNum]

def getDriverMonthStatistics(offNum, month):
    with open('data/data/statistics.json', 'r', encoding='utf-8') as statisticsFile:
        STATISTICS = json.load(statisticsFile)

    if (offNum not in STATISTICS):
        return getEmptyStatisticsMonthDict()
    offNumDict = STATISTICS[offNum]
    if (month not in offNumDict):
        return getEmptyStatisticsMonthDict()
    return offNumDict[month]