import pdfplumber
import zlib

from src.share.filenames import WEEK_SERVICES_BY_DRIVER_ENCRYPTED_PDF_PATH, WEEK_SERVICES_BY_DRIVER_ENCRYPTED_PATH

def calculateHash(serviceKeys):
    hash = 0
    sign = 1
    for serviceKey in serviceKeys:
        hash = (hash + sign * zlib.adler32(str.encode(serviceKey)))
        sign = sign * -1
    return hash

def extractRulesByDriverAndCalculateServicesHash():
    # already downloaded in ConfigureDaysAndWeekSchedule cp
    PDFFile = WEEK_SERVICES_BY_DRIVER_ENCRYPTED_PDF_PATH
    with pdfplumber.open(PDFFile) as PDF:
        fileW = open(WEEK_SERVICES_BY_DRIVER_ENCRYPTED_PATH, 'w', encoding='utf-8')
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




