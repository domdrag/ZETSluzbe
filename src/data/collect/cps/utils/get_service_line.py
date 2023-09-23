import ast
import datetime

def getServiceLine(serviceNum, dayIndex, weekSchedule, mondayDate, workDayFileNames):
    if(not serviceNum.isnumeric()):
        return [serviceNum]

    if(weekSchedule[dayIndex] == 'W'):
        textFileName = 'data/data/rules_W.txt'
        day = (mondayDate + datetime.timedelta(days = dayIndex)).day
        for workDayFileName in workDayFileNames:
            if (workDayFileName == 'rules_W'):
                continue
            # fileName starts with rules_W
            specificDays = ast.literal_eval(workDayFileName[7:])
            if (day in specificDays):
                textFileName = 'data/data/' + workDayFileName + '.txt'
                break
        fileR = open(textFileName, 'r', encoding='utf-8')
    elif(weekSchedule[dayIndex] == 'St'):
        fileR = open('data/data/rules_ST.txt', 'r', encoding='utf-8')
    else:
        fileR = open('data/data/rules_SN.txt', 'r', encoding='utf-8')

    serviceLines = fileR.readlines()
    fileR.close()
    for serviceLine in serviceLines:
        serviceLine = ast.literal_eval(serviceLine)
        if(serviceNum in serviceLine):
            return serviceLine

    return []
