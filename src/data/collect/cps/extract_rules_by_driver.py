import pdfplumber
import zlib

from src.data.collect.cps.utils.determine_week_schedule import (
    determineWeekSchedule
    )

def calculateHash(serviceKeys):
    hash = 0
    sign = 1
    for serviceKey in serviceKeys:
        hash = (hash + sign * zlib.adler32(str.encode(serviceKey)))
        sign = sign * -1
    return hash

def extractRulesByDriver(weekSchedule, mondayDate):
    PDFFile = 'data/data/tpd.pdf' # downloaded in configure_days util
    with pdfplumber.open(PDFFile) as PDF:
        determineWeekSchedule(PDF.pages[0], weekSchedule, mondayDate)       
        fileW = open('data/data/week_services_by_driver_encrypted.txt',
                     'w',
                     encoding='utf-8')

        fullHash = 0
        for page in PDF.pages:            
            tables = page.dedupe_chars().find_tables()
            for tableId in tables:
                table = tableId.extract()
                for services in table:
                    if(isinstance(services[0], str) and services[0].isnumeric()):
                        if(not services[0]):
                            continue
                        fullHash = fullHash + calculateHash(services[0:8])
                        fileW.write(f"{services[0:8]}\n")
                        if(not services[8]):
                            continue
                        fullHash = fullHash + calculateHash(services[8:])
                        fileW.write(f"{services[8:]}\n")
        fileW.close()

    return {'servicesHash': fullHash}




