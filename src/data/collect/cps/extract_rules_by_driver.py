import pdfplumber
import zlib

def calculateHash(serviceKeys):
    hash = 0
    sign = 1
    for serviceKey in serviceKeys:
        hash = (hash + sign * zlib.adler32(str.encode(serviceKey)))
        sign = sign * -1
    return hash

def extractRulesByDriverAndCalculateServicesHash():
    PDFFile = 'data/data/tpd.pdf' # already downloaded in ConfigureDaysAndWeekSchedule cp
    with pdfplumber.open(PDFFile) as PDF:
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




