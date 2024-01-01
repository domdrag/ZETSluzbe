import ast
import datetime

from src.share.filenames import (CENTRAL_DATA_DIR, PRIMARY_WORK_DAY_RULES_PATH, PRIMARY_SATURDAY_RULES_PATH,
                                 PRIMARY_SUNDAY_RULES_FILE_PATH, PRIMARY_WORK_DAY_RULES_FILE_PREFIX,
                                 PRIMARY_SATURDAY_RULES_FILE_PREFIX, PRIMARY_SUNDAY_RULES_FILE_PREFIX)
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
                fileNamePath = CENTRAL_DATA_DIR + fileName + '.txt'
                break

    if (not fileNamePath):
        if (weekSchedule[dayIndex] == 'W'):
            ASSERT_THROW(PRIMARY_WORK_DAY_RULES_FILE_PREFIX in fileNames,
                         'No generic rules for WorkDays generated.')
            fileNamePath = PRIMARY_WORK_DAY_RULES_PATH
        elif (weekSchedule[dayIndex] == 'ST'):
            ASSERT_THROW(PRIMARY_SATURDAY_RULES_FILE_PREFIX in fileNames,
                         'No generic rules for Saturday generated.')
            fileNamePath = PRIMARY_SATURDAY_RULES_PATH
        else:
            ASSERT_THROW(PRIMARY_SUNDAY_RULES_FILE_PREFIX in fileNames,
                         'No generic rules for Sunday generated.')
            fileNamePath = PRIMARY_SUNDAY_RULES_FILE_PATH

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
