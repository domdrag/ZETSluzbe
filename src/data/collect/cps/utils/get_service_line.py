import ast
import datetime

from src.share.asserts import ASSERT_THROW
from src.share.trace import TRACE

def getFormattedDateStr(date):
    dateStr = str(date)
    return '-'.join(reversed(dateStr.split('-')))

def getServiceLine(serviceNum, dayIndex, weekSchedule, mondayDate, fileNames, enableTraces = False):
    if (not serviceNum.isnumeric()):
        return [serviceNum]

    fileNamePath = ''
    date = mondayDate + datetime.timedelta(days=dayIndex)
    day = date.day
    for fileName in fileNames:
        if ('[' in fileName):
            rangeListStartIndex = fileName.index('[')
            specificDays = ast.literal_eval(fileName[rangeListStartIndex:])
            if (day in specificDays):
                fileNamePath =  'data/data/' + fileName + '.txt'
                break

    if (not fileNamePath):
        if (weekSchedule[dayIndex] == 'W'):
            ASSERT_THROW('rules_W' in fileNames, 'No generic rules for WorkDays generated.')
            fileNamePath = 'data/data/rules_W.txt'
        elif (weekSchedule[dayIndex] == 'ST'):
            ASSERT_THROW('rules_ST' in fileNames, 'No generic rules for Saturday generated.')
            fileNamePath = 'data/data/rules_ST.txt'
        else:
            ASSERT_THROW('rules_SN' in fileNames, 'No generic rules for Sunday generated.')
            fileNamePath = 'data/data/rules_SN.txt'

    if (enableTraces):
        formattedDateStr = getFormattedDateStr(date)
        TRACE('For date: ' + formattedDateStr + ' selected file: ' + fileNamePath)
        return

    fileR = open(fileNamePath, 'r', encoding='utf-8')
    serviceLines = fileR.readlines()
    fileR.close()
    for serviceLine in serviceLines:
        serviceLine = ast.literal_eval(serviceLine)
        if (serviceNum in serviceLine):
            return serviceLine

    return []
