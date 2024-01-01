import ast
import os
import zipfile

from src.data.collect.cps.utils.get_service_layout import getServiceLayoutAndUpdateStats
from src.data.collect.cps.utils.get_service_line import getServiceLine
from src.data.manager.statistics_manager import StatisticsManager
from src.data.manager.warning_messages_manager import WarningMessagesManager
from src.data.share.get_service_date import getServiceDate
from src.data.share.decompress_services import decompressServicesFile
from src.share.filenames import (CENTRAL_DATA_DIR, COMPRESSED_SERVICES_PATH, COMPRESSED_UPDATED_SERVICES_PATH,
                                 WEEK_SERVICES_BY_DRIVER_ENCRYPTED_PATH)
from src.share.trace import TRACE

def configureEmptyServices():
    return [None] * 7

def configureValidOldServicesIndexed(filePath, mondayDate):
    fileR = open(filePath, 'r', encoding='utf-8')
    services = fileR.readlines()
    fileR.close()

    currServiceIndex = -1
    validOldServicesUnordered = []
    while (getServiceDate(ast.literal_eval(services[currServiceIndex])) >= mondayDate):
        validOldServicesUnordered.append(ast.literal_eval(services[currServiceIndex]))
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

def compressServicesFile(servicesFile):
    with zipfile.ZipFile(COMPRESSED_UPDATED_SERVICES_PATH,
                         'a',
                         zipfile.ZIP_DEFLATED) as updatedServicesZIP:
        updatedServicesZIP.write(CENTRAL_DATA_DIR + servicesFile, servicesFile)

def addOldServicesWithNoUpdate():
    servicesZIP = zipfile.ZipFile(COMPRESSED_SERVICES_PATH, 'r', zipfile.ZIP_DEFLATED)
    updatedServicesZIP = zipfile.ZipFile(COMPRESSED_UPDATED_SERVICES_PATH, 'r', zipfile.ZIP_DEFLATED)
    servicesWithNoUpdate = set(servicesZIP.namelist()) - set(updatedServicesZIP.namelist())
    for serviceFile in servicesWithNoUpdate:
        decompressServicesFile(serviceFile)
        compressServicesFile(serviceFile)
        os.remove(CENTRAL_DATA_DIR + serviceFile)

def addDecryptedServices(days, weekSchedule, mondayDate, fileNames):
    zipfile.ZipFile(COMPRESSED_UPDATED_SERVICES_PATH, 'w', zipfile.ZIP_DEFLATED)
    fileR = open(WEEK_SERVICES_BY_DRIVER_ENCRYPTED_PATH, 'r', encoding='utf-8')
    weekServicesALL = fileR.readlines()
    fileR.close()

    alreadyFoundMissingService = False
    for weekServicesRaw in weekServicesALL:
        weekServices = ast.literal_eval(weekServicesRaw)
        offNum = int(weekServices[0])
        servicesFile = str(offNum) + '.txt'
        decompressServicesFile(servicesFile)
        filePath = CENTRAL_DATA_DIR + servicesFile
        newColleague = False

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
            newColleague = True
            fileW = open(filePath, 'w', encoding='utf-8')

        for i in range(1,8):
            if (not newColleague and validOldServicesIndexed[i-1]):
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
        compressServicesFile(servicesFile)
        os.remove(filePath)

    addOldServicesWithNoUpdate()
    os.remove(COMPRESSED_SERVICES_PATH)
    os.rename(COMPRESSED_UPDATED_SERVICES_PATH, COMPRESSED_SERVICES_PATH)
    StatisticsManager.finishUpdate()
    return {'missingServices': alreadyFoundMissingService}

