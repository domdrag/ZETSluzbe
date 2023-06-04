import pdfplumber

from src.data.admin.utils.download_pdf_file import downloadPDFFile

def determineRemovingRectsColor(typeOfDay):
    if (typeOfDay == 'work_day'):
        return (0,0,1)
    elif (typeOfDay == 'saturday'):
        return (0, 0.502, 0)
    else:
        return (1,0,0)

#### thanks to jsvine - owner of pdfplumber
def extractRule(typeOfDay, URL, fileName):
    PDFFile = downloadPDFFile(URL, fileName)
    with pdfplumber.open(PDFFile) as PDF:
        fileW = open('data/data/rules_' + typeOfDay + '.txt',
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

def extractRules(workDayURL, saturdayURL, sundayURL):
    extractRule('work_day', workDayURL, 'workDay.pdf')
    extractRule('saturday', saturdayURL, 'saturday.pdf')
    extractRule('sunday', sundayURL, 'sunday.pdf')
