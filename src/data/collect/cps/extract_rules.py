import pdfplumber
import re
import ast
from datetime import date, timedelta

from src.data.collect.cps.utils.download_pdf_file import downloadPDFFile
from src.data.manager.warning_messages_manager import WarningMessagesManager
from src.data.collect.cps.utils.regex_definitions import RegexDefinitions
from src.data.collect.cps.utils.get_service_line import getServiceLine
from src.share.filenames import (CENTRAL_DATA_DIR, PRIMARY_WORK_DAY_RULES_FILE_PREFIX,
                                 PRIMARY_SATURDAY_RULES_FILE_PREFIX, PRIMARY_SUNDAY_RULES_FILE_PREFIX,
                                 PRIMARY_SPECIAL_RULES_FILE_PREFIX)
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
    numOfTills = linkName.count(' do ')
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
            tillStrIndex = linkName.find('do', matchIndexStart, matchIndexEnd)
            dashStrIndex = linkName.find('-', matchIndexStart, matchIndexEnd)
            if (tillStrIndex > dashStrIndex):
                rangeSeparatorStr = 'do'
            else:
                rangeSeparatorStr = '-'
            actualDateStrings = daysRangeStr.split(rangeSeparatorStr)
            startDateStr = actualDateStrings[0] + year + '.'
            endDateStr = actualDateStrings[1]
            daysInTarget = getDaysInRange(startDateStr, endDateStr)

        # 4) xx. -/do xx. xx. xxxx.
        elif (daysRangeRegexMatch):
            daysRangeStr = daysRangeRegexMatch.group(0)
            matchIndexStart = linkName.find(daysRangeStr)
            matchIndexEnd = matchIndexStart + len(daysRangeStr)
            tillStrIndex = linkName.find('do', matchIndexStart, matchIndexEnd)
            dashStrIndex = linkName.find('-', matchIndexStart, matchIndexEnd)
            if (tillStrIndex > dashStrIndex):
                rangeSeparatorStr = 'do'
            else:
                rangeSeparatorStr = '-'
            actualDateStrings = daysRangeStr.split(rangeSeparatorStr)
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

# Custom exception
# Uses:
## 1) No rules link found - use old resources if possible
## 2) No PDF present on the rules link - use old resources if possible
## 3) Found old special day rules link - ignore it
class ExtractRulesCustomException(Exception):
    pass

def determineTypeOfDayForSpecialDays(fileName, mondayDate, weekSchedule):
    ASSERT_THROW(fileName.find('[') != -1, 'Invalid specialDay fileName.')
    rangeListStartIndex = fileName.index('[')
    specificDays = ast.literal_eval(fileName[rangeListStartIndex:])
    dayToFind = specificDays[0]  # any day should work
    dayIndex = -3 # usually we are updating in Friday -> need to consider extra 3 days in case special days are
                  ## referring to old Friday, old Saturday and/or old Sunday
    
    while dayIndex < 7:
        nextDate = mondayDate + timedelta(days=dayIndex)
        if (nextDate.day == dayToFind):
            break
        dayIndex += 1

    if (dayIndex == 7):
        TRACE('Found old rules file for special day')
        raise ExtractRulesCustomException('Ignoring old special day rules file')

    TRACE('For file: ' + fileName + ' determined typeOfDay: ' + weekSchedule[dayIndex])
    return weekSchedule[dayIndex]


def determineRemovingRectsColor(typeOfDay):
    if (typeOfDay == 'W'):
        return (0,0,1)
    elif (typeOfDay == 'ST'):
        return (0, 0.502, 0)
    else:
        return (1,0,0)

def duplicatesExist(container):
    return len(container) != len(set(container))

#### thanks to jsvine - owner of pdfplumber
def extractRule(typeOfDay, URL, fileName):
    try:
        PDFFile = downloadPDFFile(URL, CENTRAL_DATA_DIR, fileName + '.pdf')
    except Exception as e:
        raise ExtractRulesCustomException(e)

    with pdfplumber.open(PDFFile) as PDF:
        fileW = open(CENTRAL_DATA_DIR + fileName + '.txt', 'w', encoding='utf-8')
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

def getFormattedDateStr(date):
    dateStr = str(date)
    return '-'.join(reversed(dateStr.split('-')))

def mustUseOldResources(weekSchedule, typeOfDay, specialDays, mondayDate, potentialErrorMessage):
    mustUse = False

    for dayIndex in range(len(weekSchedule)):
        if weekSchedule[dayIndex] != typeOfDay:
            continue

        date = mondayDate + timedelta(days=dayIndex)
        if (date.day not in specialDays):
            formattedDateStr = getFormattedDateStr(date)
            TRACE('Potential error: ' + potentialErrorMessage)
            TRACE('Will use fallback to old resources for ' + formattedDateStr)
            mustUse = True

    return mustUse

def extractRules(workDayLinks,
                 saturdayLinks,
                 sundayLinks,
                 specialDayLinks,
                 weekSchedule,
                 mondayDate,
                 canUseOldWorkDayResources,
                 canUseOldSaturdayResources,
                 canUseOldSundayResources):
    fileNames = []
    specialDays = set()

    # SPECIAL DAY
    if (specialDayLinks):
        WarningMessagesManager.addWarningMessage('Nadjene sluzbe za posebni/e datum/e.')
    for link in specialDayLinks:
        fileNameSPPrefix = PRIMARY_SPECIAL_RULES_FILE_PREFIX
        fileNameSP = determineRulesFileName(link['name'], fileNameSPPrefix)
        try:
            typeOfDaySP = determineTypeOfDayForSpecialDays(fileNameSP, mondayDate, weekSchedule)
        except ExtractRulesCustomException as e:
            TRACE(e)
            continue

        fileNames.append(fileNameSP)
        rangeListStartIndex = fileNameSP.index('[')
        specialDays.update(ast.literal_eval(fileNameSP[rangeListStartIndex:]))

        TRACE('Extracting rules for file: ' + fileNameSP + ', typeOfDay: ' + typeOfDaySP)
        extractRule(typeOfDaySP, link['URL'], fileNameSP)

    # WORK DAY
    try:
        typeOfDayW = 'W'
        fileNameWPrefix = PRIMARY_WORK_DAY_RULES_FILE_PREFIX

        if (not workDayLinks):
            raise ExtractRulesCustomException('No workDay links found')

        # Currently only 1 workDay link supported, if ever opt for multiple need to refactor
        ## ExtractRulesCustomException handling since extractRule might raise e.g. for only one
        ## workDay link
        for link in workDayLinks:
            fileNameW = determineRulesFileName(link['name'], fileNameWPrefix)
            TRACE('Extracting rules for file: ' + fileNameW + ', typeOfDay: ' + typeOfDayW)
            extractRule(typeOfDayW, link['URL'], fileNameW)
            fileNames.append(fileNameW)
    except ExtractRulesCustomException as p:
        # No links found or PDF not present on the link
        if (not mustUseOldResources(weekSchedule, typeOfDayW, specialDays, mondayDate, str(p))):
            pass
        elif (canUseOldWorkDayResources):
            fileNames.append(fileNameWPrefix)
            WarningMessagesManager.addWarningMessage('Koristenje starih resursa za Radni dan!')
        else:
            raise Exception(p)

    # SATURDAY
    try:
        typeOfDayST = 'ST'
        fileNameST = PRIMARY_SATURDAY_RULES_FILE_PREFIX

        if (not saturdayLinks):
            raise ExtractRulesCustomException('No saturday links found')

        # Currently only 1 Saturday link supported, if ever opt for multiple need to refactor
        ## ExtractRulesCustomException handling since extractRule might raise e.g. for only one
        ## Saturday link
        for link in saturdayLinks:
            TRACE('Extracting rules for file: ' + fileNameST + ', typeOfDay: ' + typeOfDayST)
            extractRule(typeOfDayST, link['URL'], fileNameST)
            fileNames.append(fileNameST)
    except ExtractRulesCustomException as p:
        # No links found or PDF not present on the link
        if (not mustUseOldResources(weekSchedule, typeOfDayST, specialDays, mondayDate, str(p))):
            pass
        elif (canUseOldSaturdayResources):
            fileNames.append(fileNameST)
            WarningMessagesManager.addWarningMessage('Koristenje starih resursa za Subotu!')
        else:
            raise Exception(p)

    # SUNDAY
    try:
        typeOfDaySN = 'SN'
        fileNameSN = PRIMARY_SUNDAY_RULES_FILE_PREFIX

        if (not sundayLinks):
            raise ExtractRulesCustomException('No sunday links found')

        # Currently only 1 Sunday link supported, if ever opt for multiple need to refactor
        ## ExtractRulesCustomException handling since extractRule might raise e.g. for only one
        ## Sunday link
        for link in sundayLinks:
            TRACE('Extracting rules for file: ' + fileNameSN + ', typeOfDay: ' + typeOfDaySN)
            extractRule(typeOfDaySN, link['URL'], fileNameSN)
            fileNames.append(fileNameSN)
    except ExtractRulesCustomException as p:
        # No links found or PDF not present on the link
        if (not mustUseOldResources(weekSchedule, typeOfDaySN, specialDays, mondayDate, str(p))):
            pass
        elif (canUseOldSundayResources):
            fileNames.append(fileNameSN)
            WarningMessagesManager.addWarningMessage('Koristenje starih resursa za Nedjelju!')
        else:
            raise Exception(p)

    if (duplicatesExist(fileNames)):
        raise Exception('Multiple work day files with the same name')
    getTracesForGetServiceLineMethod(weekSchedule, mondayDate, fileNames)

    return fileNames