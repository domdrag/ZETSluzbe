import ast

from src.data.admin.utils.get_service_layout import getServiceLayoutAndUpdateStats
from src.data.admin.utils.get_service_line import getServiceLine
from src.data.admin.utils.statistics_manager import setStatistics
from src.data.admin.utils.count_previously_added_services import countPreviouslyAddedServices
from src.data.share.config_manager import getConfig

def configureEmptyServices():
    return [None] * 7

def configureValidOldIndexedServices(filePath, oldMissingServices, numOfPreviouslyAddedServices):
    fileR = open(filePath, 'r', encoding='utf-8')
    services = fileR.readlines()
    fileR.close()

    validOldServices = configureEmptyServices()
    validOldServicesUnordered = services[-numOfPreviouslyAddedServices:]
    currValidOldServIndex = 0
    for i in range(len(oldMissingServices)):
        if (not oldMissingServices[i]):
            validOldServices[i] = validOldServicesUnordered[currValidOldServIndex]
            currValidOldServIndex = currValidOldServIndex + 1

    return validOldServices

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

def addDecryptedServices(days,
                         weekSchedule,
                         missingServices,
                         updateCause,
                         mondayDate,
                         workDayFileNames):
    fileR = open('data/data/week_services_by_driver_encrypted.txt',
                 'r',
                 encoding='utf-8')
    weekServicesALL = fileR.readlines()
    fileR.close()

    for weekServicesRaw in weekServicesALL:
        weekServices = ast.literal_eval(weekServicesRaw)
        offNum = int(weekServices[0])
        filePath = 'data/data/all_services_by_driver_decrypted/' \
                    + str(offNum) \
                    + '.txt'

        if (updateCause == 'MISSING_SERVICES'):
            config = getConfig()
            oldMissingServices = config['MISSING_SERVICES']
            numOfPreviouslyAddedServices = countPreviouslyAddedServices(oldMissingServices)
            validOldIndexedServices = configureValidOldIndexedServices(filePath,
                                                                       oldMissingServices,
                                                                       numOfPreviouslyAddedServices)
            deletePreviouslyAddedServices(filePath, numOfPreviouslyAddedServices)
        else:
            validOldIndexedServices = configureEmptyServices()

        fileW = open(filePath, 'a', encoding='utf-8')
        for i in range(1,8):
            if (validOldIndexedServices[i-1]):
                # already contains newline
                fileW.write(validOldIndexedServices[i-1])
                continue
            if (missingServices[i-1]):
                continue

            serviceNum = weekServices[i]
            serviceLine = getServiceLine(serviceNum, i-1, weekSchedule, mondayDate, workDayFileNames)
            serviceLayout = getServiceLayoutAndUpdateStats(serviceLine, serviceNum, days, i-1, str(offNum))
            fileW.write(f"{serviceLayout}\n")
        fileW.close()

    setStatistics()


