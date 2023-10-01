import pdfplumber

from src.data.collect.cps.utils.download_pdf_file import downloadPDFFile
from src.data.collect.cps.utils.add_warning_message import addWarningMessage
from src.share.asserts import ASSERT_THROW
from src.share.trace import TRACE

def determineWorkDayFileName(linkName, numOfWorkDayLinks):
    if (numOfWorkDayLinks == 1):
        return 'rules_W'

    isOrdinal = lambda word: word[:-1].isdigit() and word[-1] == '.'
    # we want to split every dot as well, but also keep the dot to be sure which numbers are dates
    linkName = linkName.replace('.', '. ')
    words = linkName.split()
    prevWordOrdinal = False
    prevWordAppended = False
    potentialDays = []
    ordinals = []

    for word in words:
        if (isOrdinal(word)):
            number = int(word[:-1])
            if (not prevWordOrdinal and 0 < number < 32):
                potentialDays.append(number)
                prevWordAppended = True
            else:
                # prev word is ordinal or number is year
                if (prevWordAppended and number > 2000):
                    potentialDays = potentialDays[:-1]
                prevWordAppended = False

            prevWordOrdinal = True
            ordinals.append(int(word[:-1]))
        else:
            if (prevWordAppended and (word == 'mjesec' or word == 'Mjesec')):
                potentialDays = potentialDays[:-1]
            prevWordOrdinal = False
            prevWordAppended = False

    if ('od' in linkName or 'Od' in linkName or 'OD' in linkName):
        if ('do' in linkName or 'Do' in linkName or 'DO' in linkName or '-' in linkName):
            ASSERT_THROW(len(potentialDays) == 2, 'Sustav nije razumio linkove za radne dane.')
            daysRange = list(range(min(potentialDays), max(potentialDays) + 1))
            return 'rules_W' + str(daysRange)
        else:
            ASSERT_THROW(len(potentialDays) == 1, 'Sustav nije razumio linkove za radne dane.')
            return 'rules_W'
    else:
        return 'rules_W' + str(potentialDays)

def determineRemovingRectsColor(typeOfDay):
    if (typeOfDay == 'work_day'):
        return (0,0,1)
    elif (typeOfDay == 'saturday'):
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

def extractRules(workDayLinks, saturdayLinks, sundayLinks, canUseOldWorkDayResources):
    fileNames = {'workDay': []}

    # WORK DAY
    try:
        if (not workDayLinks):
            raise PotentialException('No workDay links found')
        if (len(workDayLinks) > 1):
            addWarningMessage('Nadjeno vise rasporeda za radni dan!')
        for link in workDayLinks:
            fileName = determineWorkDayFileName(link['name'], len(workDayLinks))
            extractRule('work_day', link['URL'], fileName)
            fileNames['workDay'].append(fileName)
        if (duplicatesExist(fileNames['workDay'])):
            raise Exception('Multiple work day files with the same name')
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
        for link in saturdayLinks:
            extractRule('saturday', link['URL'], 'rules_ST')
    except PotentialException as p:
        # No links found or PDF not present on the link
        TRACE('Potential error: ' + str(p))
        TRACE('Using old resources for Saturday')
        addWarningMessage('Koristenje starih resursa za Subotu!')

    # SUNDAY
    try:
        if (not sundayLinks):
            raise PotentialException('No sunday links found')
        for link in sundayLinks:
            extractRule('sunday', link['URL'], 'rules_SN')
    except PotentialException as p:
        # No links found or PDF not present on the link
        TRACE('Potential error: ' + str(p))
        TRACE('Using old resources for Sunday')
        addWarningMessage('Koristenje starih resursa za Nedjelju!')

    return fileNames