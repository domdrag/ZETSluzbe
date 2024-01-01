import pdfplumber
import datetime
import re
from datetime import date

from src.data.collect.cps.utils.download_pdf_file import downloadPDFFile
from src.data.collect.cps.utils.configure_week_schedule import configureWeekSchedule
from src.share.filenames import CENTRAL_DATA_DIR, WEEK_SERVICES_BY_DRIVER_ENCRYPTED_PDF_FILE
from src.share.trace import TRACE

def getStringDate(date):
    return str(date.day) + '.' + str(date.month) + '.' + str(date.year) + '.'

def getMondayDate(textFirstPDF):
    odIndex = textFirstPDF.find('od')
    stringForMonth = textFirstPDF[odIndex:odIndex + 50]
    stringForMonthList = re.split(' |\.', stringForMonth)
    day = stringForMonthList[1]
    month = stringForMonthList[2]
    year = stringForMonthList[3]
    mondayDate = date(int(year), int(month), int(day))
    return mondayDate

def configureDays(days, mondayDate):
    monday = 'Ponedjeljak, ' + getStringDate(mondayDate)
    nextDate = mondayDate + datetime.timedelta(days = 1)
    tuesday = 'Utorak, ' + getStringDate(nextDate)
    nextDate = nextDate + datetime.timedelta(days = 1)
    wednesday = 'Srijeda, ' + getStringDate(nextDate)
    nextDate = nextDate + datetime.timedelta(days = 1)
    thursday = 'Cetvrtak, ' + getStringDate(nextDate)
    nextDate = nextDate + datetime.timedelta(days = 1)
    friday = 'Petak, ' + getStringDate(nextDate)
    nextDate = nextDate + datetime.timedelta(days = 1)
    saturday = 'Subota, ' + getStringDate(nextDate)
    nextDate = nextDate + datetime.timedelta(days = 1)
    sunday = 'Nedjelja, ' + getStringDate(nextDate)

    days.append(monday)
    days.append(tuesday)
    days.append(wednesday)
    days.append(thursday)
    days.append(friday)
    days.append(saturday)
    days.append(sunday)
    return mondayDate

def configureDaysAndWeekSchedule(allServicesURL, weekSchedule, days):
    PDFFile = downloadPDFFile(allServicesURL, CENTRAL_DATA_DIR, WEEK_SERVICES_BY_DRIVER_ENCRYPTED_PDF_FILE)
    with pdfplumber.open(PDFFile) as PDF:
        page = PDF.pages[0]
        textFirstPDF = page.extract_text()

    mondayDate = getMondayDate(textFirstPDF)
    configureDays(days, mondayDate)
    configureWeekSchedule(page, weekSchedule, mondayDate)
    TRACE('Configured week schedule: ' + str(weekSchedule))
    TRACE('----------------------------------------')
    return {'mondayDate': mondayDate}

