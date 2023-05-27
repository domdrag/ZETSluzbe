import ast

def getHolidays():
    filePath = 'data/data/holidays.txt'
    weekServices = ''
    
    try:
        fileR = open(filePath, 'r', encoding='utf-8')
        holidays = fileR.readlines()
        fileR.close()
    except:
        return []

    holidayData = []
    for holidayRawString in holidays:
        holiday = ast.literal_eval(holidayRawString)
        holidayData.append(holiday)

    return holidayData
