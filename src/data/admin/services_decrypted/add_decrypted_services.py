import ast

from src.data.admin.utils.get_service_layout import getServiceLayoutAndUpdateStats
from src.data.admin.utils.get_service_line import getServiceLine
from src.data.admin.utils.statistics_manager import setStatistics
from src.data.share.config_manager import getConfig

def deletePreviouslyAddedServices(filePath, numOfPreviouslyAddedServices):
    fileR = open(filePath, 'r', encoding='utf-8')
    services = fileR.readlines()
    fileR.close()

    numOfServices = len(services)
    numOfKeptServices = numOfServices - numOfPreviouslyAddedServices

    fileW = open(filePath, 'w', encoding='utf-8')
    for i in range(numOfKeptServices):
        fileW.write(services[i])
    fileW.close()

def addDecryptedServices(days, weekSchedule, numOfPreviouslyAddedServicesSetToDelete = None):
    fileR = open('data/data/week_services_by_driver_encrypted.txt',
                 'r',
                 encoding='utf-8')
    weekServicesALL = fileR.readlines()
    fileR.close()

    config = getConfig()
    missingServices = config['MISSING_SERVICES']
    for weekServicesRaw in weekServicesALL:
        weekServices = ast.literal_eval(weekServicesRaw)
        offNum = int(weekServices[0])
        filePath = 'data/data/all_services_by_driver_decrypted/' \
                    + str(offNum) \
                    + '.txt'
        if (numOfPreviouslyAddedServicesSetToDelete):
            deletePreviouslyAddedServices(filePath, numOfPreviouslyAddedServicesSetToDelete)

        fileW = open(filePath, 'a', encoding='utf-8')
        for i in range(1,8):
            if (missingServices[i-1]):
                continue

            serviceNum = weekServices[i]
            serviceLine = getServiceLine(serviceNum, i-1, weekSchedule)
            serviceLayout = getServiceLayoutAndUpdateStats(serviceLine, serviceNum, days, i-1, str(offNum))
            fileW.write(f"{serviceLayout}\n")
        fileW.close()
    setStatistics()

def addMissingDecryptedServices(days, weekSchedule, numOfPreviouslyAddedServices):
    addDecryptedServices(days, weekSchedule, numOfPreviouslyAddedServices)

