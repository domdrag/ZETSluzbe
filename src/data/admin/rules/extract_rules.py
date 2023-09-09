import pdfplumber

from src.data.share.download_pdf_file import downloadPDFFile

def determineWorkDayFileName(linkName):
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
            assert len(potentialDays) == 2, 'Sustav nije razumio linkove za radne dane.'
            daysRange = list(range(min(potentialDays), max(potentialDays) + 1))
            return 'rules_W' + str(daysRange)
        else:
            assert len(potentialDays) == 1, 'Sustav nije razumio linkove za radne dane.'
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

#### thanks to jsvine - owner of pdfplumber
def extractRule(typeOfDay, URL, fileName):
    PDFFile = downloadPDFFile(URL, 'data/data/', fileName + '.pdf')
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

def extractRules(workDayLinks, saturdayLinks, sundayLinks):
    fileNames = {'workDay' : []}

    for link in workDayLinks:
        fileName = 'rules_W'
        if (len(workDayLinks) > 1):
            fileName = determineWorkDayFileName(link['name'])
        extractRule('work_day', link['URL'], fileName)
        fileNames['workDay'].append(fileName)

    for link in saturdayLinks:
        extractRule('saturday', link['URL'], 'rules_ST')

    for link in sundayLinks:
        extractRule('sunday', link['URL'], 'rules_SN')

    return fileNames