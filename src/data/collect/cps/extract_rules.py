import pdfplumber
import re
import ast
from datetime import date, timedelta

from src.data.collect.cps.utils.download_pdf_file import downloadPDFFile
from src.data.collect.cps.utils.add_warning_message import addWarningMessage
from src.data.collect.cps.utils.regex_definitions import RegexDefinitions
from src.data.collect.cps.utils.get_service_line import getServiceLine
from src.share.asserts import ASSERT_THROW
from src.share.trace import TRACE

def extractDay(date):
    return int(date.split('.')[0])

def getDaysInRange(dateStart, dateEnd):
    dateStartTerms = dateStart.split('.')
    dateEndTerms = dateEnd.split('.')
    dateStartTyped = date(int(dateStartTerms[2]),
                          int(dateStartTerms[1]),
                          int(dateStartTerms[0]))
    dateEndTyped = date(int(dateEndTerms[2]),
                        int(dateEndTerms[1]),
                        int(dateEndTerms[0]))
    datesInRange = dateEndTyped - dateStartTyped
    daysInRange = []
    for i in range(datesInRange.days + 1):
        dateInRange = dateStartTyped + timedelta(days = i)
        daysInRange.append(dateInRange.day)
    return daysInRange

def getDaysFromDates(dates):
    days = []
    for date in dates:
        days.append(extractDay(date))
    return list(set(days))

### TYPES OF RULES LINKS WITH DATES IN NAME
# # Space in-between allowed
# # 1) xx.xx.xxxx.
# # 2) xx.xx.xxxx.(,)( )xx.xx.xxxx(,)( )...
# # 3) xx., xx., ... xx. xx. xxxx. [daysListRegex]
# # 4) xx. -/do xx. xx. xxxx. [daysRangeRegex]
# # 5) xx. xx. -/do xx. xx. xxxx. [daysRangeDiffMonthRegex]
# # 6) (od) xx.xx.xxxx. -/do xx.xx.xxxx.

def determineRulesFileName(linkName, fileNamePrefix):
    numOfDashes = linkName.count('-')
    numOfTills = linkName.count('do')
    ASSERT_THROW(numOfDashes + numOfTills < 2,
                 'Invalid rules linkName: ' + linkName)

    datePatternFinder = re.compile(RegexDefinitions.dateRegex)
    # findall does not work with overlaps i.e. daysListRegex
    dateStrings = datePatternFinder.findall(linkName)
    daysInTarget = []

    # 2) xx.xx.xxxx., xx.xx.xxxx, ...
    if (len(dateStrings) >= 3):
        for dateStr in dateStrings:
            daysInTarget.append(extractDay(dateStr))

    # 2), 6)
    elif (len(dateStrings) == 2):
        startDateIndex = linkName.find(dateStrings[0])
        endDateIndex = linkName.find(dateStrings[1])
        rangeSeparatorIndex = max(linkName.find('do', startDateIndex, endDateIndex),
                                  linkName.find('-', startDateIndex, endDateIndex))
        # 6) (od) xx.xx.xxxx. -/do xx.xx.xxxx.
        if (startDateIndex < rangeSeparatorIndex < endDateIndex):
            daysInTarget = getDaysInRange(dateStrings[0], dateStrings[1])
        # 2) xx.xx.xxxx., xx.xx.xxxx
        else:
            daysInTarget = getDaysFromDates(dateStrings)

    # 1), 3), 4), 5)
    elif (len(dateStrings) == 1):
        dateList = (dateStrings[0].split('.'))
        # last element will be year if there's a missing dot
        year = dateList[-1] if dateList[-1] else dateList[-2]
        month = dateList[-2] if dateList[-1] else dateList[-3]

        daysRangeDiffMonthMatch = re.search(RegexDefinitions.daysRangeDiffMonthRegex, linkName)
        daysRangeRegexMatch = re.search(RegexDefinitions.daysRangeRegex, linkName)
        daysListRegexMatch = re.search(RegexDefinitions.daysListRegex, linkName)

        # 5) xx. xx. -/do xx. xx. xxxx.
        if (daysRangeDiffMonthMatch):
            daysRangeDiffMonthStr = daysRangeDiffMonthMatch.group(0)
            matchIndexStart = linkName.find(daysRangeDiffMonthStr)
            matchIndexEnd = matchIndexStart + len(daysRangeDiffMonthStr)
            rangeSeparatorIndex = max(linkName.find('do', matchIndexStart, matchIndexEnd),
                                      linkName.find('-', matchIndexStart, matchIndexEnd))
            rangeSeparator = linkName[rangeSeparatorIndex]
            actualDateStrings = daysRangeDiffMonthStr.split(rangeSeparator)
            startDateStr = actualDateStrings[0] + year + '.'
            endDateStr = actualDateStrings[1]
            daysInTarget = getDaysInRange(startDateStr, endDateStr)

        # 4) xx. -/do xx. xx. xxxx.
        elif (daysRangeRegexMatch):
            daysRangeStr = daysRangeRegexMatch.group(0)
            matchIndexStart = linkName.find(daysRangeStr)
            matchIndexEnd = matchIndexStart + len(daysRangeStr)
            rangeSeparatorIndex = max(linkName.find('do', matchIndexStart, matchIndexEnd),
                                      linkName.find('-', matchIndexStart, matchIndexEnd))
            rangeSeparator = linkName[rangeSeparatorIndex]
            actualDateStrings = daysRangeStr.split(rangeSeparator)
            startDateStr = actualDateStrings[0] + month + '.' + year + '.'
            endDateStr = actualDateStrings[1]
            daysInTarget = getDaysInRange(startDateStr, endDateStr)

        # 3) xx., xx., ... xx. xx. xxxx.
        elif (daysListRegexMatch):
            daysListStr = daysListRegexMatch.group(0)
            actualDateStrings = daysListStr.split(',')
            for i in range(len(actualDateStrings) - 1):
                actualDateStrings[i] += month + '.' + year + '.'
            daysInTarget = getDaysFromDates(actualDateStrings)

        # 1) xx. xx. xxxx.
        else:
            if ('od' in linkName):
                return fileNamePrefix
            daysInTarget.append(extractDay(dateStrings[0]))
    else:
        raise Exception('Found rules link without date in name')

    return fileNamePrefix + str(daysInTarget) if daysInTarget else fileNamePrefix

def determineTypeOfDayForSpecialDays(fileName, mondayDate, weekSchedule):
    rangeListStartIndex = fileName.index('[')
    specificDays = ast.literal_eval(fileName[rangeListStartIndex:])
    dayToFind = specificDays[0]  # any day should work
    dayIndex = 0
    while True:
        nextDate = mondayDate + timedelta(days=dayIndex)
        if (nextDate.day == dayToFind):
            break
        dayIndex += 1
    TRACE('For file: ' + fileName + ' determined typeOfDay: ' + weekSchedule[dayIndex])
    return weekSchedule[dayIndex]


def determineRemovingRectsColor(typeOfDay):
    if (typeOfDay == 'W'):
        return (0,0,1)
    elif (typeOfDay == 'ST'):
        return (0, 0.502, 0)
    else:
        return (1,0,0)

# Custom exception for no links found or no PDF present on the link since
# we want to use old resources if possible
class PotentialException(Exception):
    pass

def duplicatesExist(container):
    return len(container) != len(set(container))

#### thanks to jsvine - owner of pdfplumber
def extractRule(typeOfDay, URL, fileName):
    try:
        PDFFile = downloadPDFFile(URL, 'data/data/', fileName + '.pdf')
    except Exception as e:
        raise PotentialException(e)

    with pdfplumber.open(PDFFile) as PDF:
        fileW = open('data/data/' + fileName + '.txt',
                     'w',
                     encoding='utf-8')
        removingColor = determineRemovingRectsColor(typeOfDay)
        for page in PDF.pages:
            filtered = (page.filter(
                lambda obj: not (obj.get("non_stroking_color") == removingColor
                                 and
                                 obj.get("width", 100) < 100)).dedupe_chars())
            tables = filtered.extract_tables()
            for table in tables:
                for serviceLine in table:
                    if(isinstance(serviceLine[0], str)
                       and serviceLine[0].isnumeric()):
                        fileW.write(f"{serviceLine}\n")
    fileW.close()
####

def getTracesForGetServiceLineMethod(weekSchedule, mondayDate, fileNames):
    serviceNumDummy = '0000'
    enableTraces = True

    for dayIndex in range(0, 7):
        getServiceLine(serviceNumDummy, dayIndex, weekSchedule, mondayDate, fileNames, enableTraces)

def extractRules(workDayLinks,
                 saturdayLinks,
                 sundayLinks,
                 specialDayLinks,
                 weekSchedule,
                 mondayDate,
                 canUseOldWorkDayResources):
    fileNames = []

    # SPECIAL DAY
    if (specialDayLinks):
        addWarningMessage('Nadjene sluzbe za posebni/e datum/e.')
    for link in specialDayLinks:
        fileNameSPPrefix = 'rules_SP'
        fileNameSP = determineRulesFileName(link['name'], fileNameSPPrefix)
        typeOfDaySP = determineTypeOfDayForSpecialDays(fileNameSP, mondayDate, weekSchedule)
        fileNames.append(fileNameSP)
        TRACE('Extracting rules for file: ' + fileNameSP + ', typeOfDay: ' + typeOfDaySP)
        extractRule(typeOfDaySP, link['URL'], fileNameSP)

    # WORK DAY
    try:
        if (not workDayLinks):
            raise PotentialException('No workDay links found')
        if (len(workDayLinks) > 1):
            addWarningMessage('Nadjeno vise rasporeda za radni dan!')
        typeOfDayW = 'W'
        for link in workDayLinks:
            fileNameWPrefix = 'rules_W'
            fileNameW = determineRulesFileName(link['name'], fileNameWPrefix)
            fileNames.append(fileNameW)
            TRACE('Extracting rules for file: ' + fileNameW + ', typeOfDay: ' + typeOfDayW)
            extractRule(typeOfDayW, link['URL'], fileNameW)
    except PotentialException as p:
        # No links found or PDF not present on the link
        TRACE('Potential error: ' + str(p))
        if (not canUseOldWorkDayResources):
            raise Exception(p)
        TRACE('Using old resources for Work Day')
        addWarningMessage('Koristenje starih resursa za Radni Dan!')

    # SATURDAY
    try:
        if (not saturdayLinks):
            raise PotentialException('No saturday links found')
        typeOfDayST = 'ST'
        for link in saturdayLinks:
            fileNameST = 'rules_ST'
            fileNames.append(fileNameST)
            TRACE('Extracting rules for file: ' + fileNameST + ', typeOfDay: ' + typeOfDayST)
            extractRule(typeOfDayST, link['URL'], fileNameST)
    except PotentialException as p:
        # No links found or PDF not present on the link
        TRACE('Potential error: ' + str(p))
        TRACE('Using old resources for Saturday')
        addWarningMessage('Koristenje starih resursa za Subotu!')

    # SUNDAY
    try:
        if (not sundayLinks):
            raise PotentialException('No sunday links found')
        typeOfDaySN = 'SN'
        for link in sundayLinks:
            fileNameSN = 'rules_SN'
            fileNames.append(fileNameSN)
            TRACE('Extracting rules for file: ' + fileNameSN + ', typeOfDay: ' + typeOfDaySN)
            extractRule(typeOfDaySN, link['URL'], fileNameSN)
    except PotentialException as p:
        # No links found or PDF not present on the link
        TRACE('Potential error: ' + str(p))
        TRACE('Using old resources for Sunday')
        addWarningMessage('Koristenje starih resursa za Nedjelju!')

    if (duplicatesExist(fileNames)):
        raise Exception('Multiple work day files with the same name')
    getTracesForGetServiceLineMethod(weekSchedule, mondayDate, fileNames)

    return fileNames