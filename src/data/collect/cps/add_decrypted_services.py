import ast
import os
import zipfile
import shutil

from src.data.collect.cps.utils.get_service_layout import getServiceLayoutAndUpdateStats
from src.data.collect.cps.utils.get_service_line import getServiceLine
from src.data.manager.statistics_manager import StatisticsManager
from src.data.manager.warning_messages_manager import WarningMessagesManager
from src.data.utils.get_service_date import getServiceDate
from src.share.trace import TRACE

ARCHIVED_DATA_PATH = 'data.zip'

def configureEmptyServices():
    return [None] * 7

def configureValidOldServicesIndexed(filePath, mondayDate):
    fileR = open(filePath, 'r', encoding='utf-8')
    services = fileR.readlines()
    fileR.close()

    currServiceIndex = -1
    validOldServicesUnordered = []
    while (getServiceDate(ast.literal_eval(services[currServiceIndex])) >= mondayDate):
        validOldServicesUnordered.append(services[currServiceIndex])
        currServiceIndex -= 1

    validOldServicesIndexed = configureEmptyServices()
    for service in validOldServicesUnordered:
        serviceDate = getServiceDate(service)
        validOldServicesIndexed[serviceDate.weekday()] = service

    return validOldServicesIndexed

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

def decompressServicesFileForOffNum(offNum):
    servicesFileInDataPath = 'all_services_by_driver_decrypted/' + offNum + '.txt'
    with zipfile.ZipFile(ARCHIVED_DATA_PATH) as dataZIP:
        with dataZIP.open(servicesFileInDataPath) as archivedServices:
            with open('data/data/' + servicesFileInDataPath, 'wb') as servicesFile:
                shutil.copyfileobj(archivedServices, servicesFile)

def compressServicesFileForOffNum(offNum):
    servicesFileInDataPath = 'all_services_by_driver_decrypted/' + offNum + '.txt'
    with zipfile.ZipFile('dataUpdated.zip', 'a', zipfile.ZIP_DEFLATED) as updatedDataZIP:
        updatedDataZIP.write('data/data/' + servicesFileInDataPath, servicesFileInDataPath)

def addDecryptedServices(days, weekSchedule, mondayDate, fileNames):
    zipfile.ZipFile('dataUpdated.zip', 'w', zipfile.ZIP_DEFLATED)
    fileR = open('data/data/week_services_by_driver_encrypted.txt',
                 'r',
                 encoding='utf-8')
    weekServicesALL = fileR.readlines()
    fileR.close()

    alreadyFoundMissingService = False
    for weekServicesRaw in weekServicesALL:
        weekServices = ast.literal_eval(weekServicesRaw)
        offNum = int(weekServices[0])
        decompressServicesFileForOffNum(str(offNum))
        filePath = 'data/data/all_services_by_driver_decrypted/' \
                    + str(offNum) \
                    + '.txt'

        if (os.path.isfile(filePath)):
            validOldServicesIndexed = configureValidOldServicesIndexed(filePath,
                                                                       mondayDate)
            numOfPreviouslyAddedServices = sum(1 for service in validOldServicesIndexed if
                                               service != None)
            if (numOfPreviouslyAddedServices):
                deletePreviouslyAddedServices(filePath, numOfPreviouslyAddedServices)
            fileW = open(filePath, 'a', encoding='utf-8')
        else:
            TRACE('New official number (new colleague) detected. OffNum: ' + str(offNum))
            fileW = open(filePath, 'w', encoding='utf-8')

        for i in range(1,8):
            if (validOldServicesIndexed[i-1]):
                # already contains newline
                fileW.write(validOldServicesIndexed[i-1])
                continue

            serviceNum = weekServices[i]
            if (not serviceNum or serviceNum == ' '):
                if (not alreadyFoundMissingService):
                    TRACE('FOUND MISSING SERVICE/S')
                    WarningMessagesManager.addWarningMessage('Nadjena/e sluzba/e koje nedostaju.')
                    alreadyFoundMissingService = True
                continue

            serviceLine = getServiceLine(serviceNum, i-1, weekSchedule, mondayDate, fileNames)
            serviceLayout = getServiceLayoutAndUpdateStats(serviceLine, serviceNum, days, i-1, str(offNum))
            fileW.write(f"{serviceLayout}\n")
        fileW.close()
        compressServicesFileForOffNum(str(offNum))
        os.remove(filePath)



