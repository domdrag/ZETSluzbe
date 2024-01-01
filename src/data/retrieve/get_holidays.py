import ast

from src.share.filenames import HOLIDAYS_PATH

def getHolidays():
    try:
        fileR = open(HOLIDAYS_PATH, 'r', encoding='utf-8')
        holidays = fileR.readlines()
        fileR.close()
    except:
        return []

    holidayData = []
    for holidayRawString in holidays:
        holiday = ast.literal_eval(holidayRawString)
        holidayData.append(holiday)

    return holidayData
