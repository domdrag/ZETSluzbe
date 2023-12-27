import ast
import os
import zipfile
import shutil

from src.data.collect.cps.utils.get_driver_info import (
    getDriverInfo
    )
from src.data.collect.cps.utils.get_service_layout import getServiceLayout
from src.data.collect.cps.utils.get_service_line import getServiceLine
from src.data.utils.get_service_date import getServiceDate

ARCHIVED_DATA_PATH = 'data.zip'

def configureEmptyShifts():
    return [None] * 7

def getValidOldShiftsUnordered(filePath, mondayDate):
    fileR = open(filePath, 'r', encoding='utf-8')
    shifts = fileR.readlines()
    fileR.close()

    validOldShiftsUnordered = []
    numOfShifts = len(shifts)
    currentIndex = numOfShifts - 1
    # REMARK: assumed currentIndex >> 0
    while(getServiceDate(ast.literal_eval(shifts[currentIndex])) >= mondayDate):
        shiftInst = shifts[currentIndex]
        shiftInstBefore = shifts[currentIndex-1]
        if (ast.literal_eval(shiftInst)[0] == ast.literal_eval(shiftInstBefore)[0]):
            shiftInstBeforeBefore = shifts[currentIndex-2]
            validOldShiftsUnordered.append([shiftInstBeforeBefore, shiftInstBefore, shiftInst])
            currentIndex = currentIndex - 3
        else:
            validOldShiftsUnordered.append([shiftInst])
            currentIndex = currentIndex - 1

    return validOldShiftsUnordered

def configureValidOldShiftsIndexed(filePath, mondayDate):
    fileR = open(filePath, 'r', encoding='utf-8')
    shifts = fileR.readlines()
    fileR.close()

    validOldShiftsUnordered = getValidOldShiftsUnordered(filePath, mondayDate)
    validOldShiftsIndexed = configureEmptyShifts()
    for shift in validOldShiftsUnordered:
        shiftDate = getServiceDate(shift[0])
        validOldShiftsIndexed[shiftDate.weekday()] = shift

    return validOldShiftsIndexed
def deletePreviouslyAddedShifts(filePath, numOfPreviouslyAddedShiftInsts):
    fileR = open(filePath, 'r', encoding='utf-8')
    shifts = fileR.readlines()
    fileR.close()

    numOfShifts = len(shifts)
    numOfKeptShifts = numOfShifts - numOfPreviouslyAddedShiftInsts

    fileW = open(filePath, 'w', encoding='utf-8')
    for i in range(numOfKeptShifts):
        fileW.write(shifts[i])
    fileW.close()

def decompressShiftsFileForOffNum(offNum):
    servicesFileInDataPath = 'all_shifts_by_driver_decrypted/' + offNum + '.txt'
    with zipfile.ZipFile(ARCHIVED_DATA_PATH) as dataZIP:
        with dataZIP.open(servicesFileInDataPath) as archivedServices:
            with open('data/data/' + servicesFileInDataPath, 'wb') as servicesFile:
                shutil.copyfileobj(archivedServices, servicesFile)

def compressShiftsFileForOffNum(offNum):
    servicesFileInDataPath = 'all_shifts_by_driver_decrypted/' + offNum + '.txt'
    with zipfile.ZipFile('dataUpdated.zip', 'a', zipfile.ZIP_DEFLATED) as updatedDataZIP:
        updatedDataZIP.write('data/data/' + servicesFileInDataPath, servicesFileInDataPath)

def addDecryptedShifts(days,
                       weekSchedule,
                       mondayDate,
                       fileNames):
    fileR = open('data/data/week_services_by_driver_encrypted.txt',
                 'r',
                 encoding='utf-8')
    weekServicesALL = fileR.readlines()
    fileR.close()

    fileR = open('data/all_drivers.txt', 'r', encoding='utf-8')
    driversRaw = fileR.readlines()
    fileR.close()
    driverList = []
    for driverRaw in driversRaw:
        driver = driverRaw.split()
        driverList.append(driver)

    for weekServicesRaw in weekServicesALL:
        weekServices = ast.literal_eval(weekServicesRaw)
        offNum = int(weekServices[0])
        decompressShiftsFileForOffNum(str(offNum))
        filePath = 'data/data/all_shifts_by_driver_decrypted/' \
                    + str(offNum) \
                    + '.txt'

        if (os.path.isfile(filePath)):
            validOldShiftsIndexed = configureValidOldShiftsIndexed(filePath,
                                                                   mondayDate)
            numOfPreviouslyAddedShiftInsts = sum(len(shift) for shift in validOldShiftsIndexed if
                                               shift != None)
            if (numOfPreviouslyAddedShiftInsts):
                deletePreviouslyAddedShifts(filePath, numOfPreviouslyAddedShiftInsts)
            fileW = open(filePath, 'a', encoding='utf-8')
        else:
            fileW = open(filePath, 'w', encoding='utf-8')

        for i in range(1,8):
            if (validOldShiftsIndexed[i-1]):
                validOldShift = validOldShiftsIndexed[i-1]
                for shiftInstance in validOldShift:
                    # already contains newline
                    fileW.write(shiftInstance)
                continue

            serviceNum = weekServices[i]
            if (not serviceNum or serviceNum == ' '):
                continue

            serviceLine = getServiceLine(serviceNum, i-1, weekSchedule, mondayDate, fileNames)
            if(len(serviceLine) == 1):
                serviceLayout = getServiceLayout(serviceLine,
                                                 serviceNum,
                                                 days,
                                                 i-1)
                fileW.write(f"{serviceLayout}\n")
                continue
            if(serviceLine == []):
                fileW.write(f"{[days[i-1], 'UNABLE TO FIND SERVICE LINE']}\n")
                continue
            for j in [0,8,15]:
                wantedServiceNum = serviceLine[j]
                serviceLayout = getServiceLayout(serviceLine,
                                                 wantedServiceNum,
                                                 days,
                                                 i-1)
                if(serviceLayout[1] == 'empty'):
                    fileW.write(f"{serviceLayout}\n")
                    continue
                driverInfo = getDriverInfo(wantedServiceNum, driverList, i)
                serviceLayout.append(driverInfo[0] + '\n' + driverInfo[1])
                fileW.write(f"{serviceLayout}\n")
        fileW.close()
        compressShiftsFileForOffNum(str(offNum))
        os.remove(filePath)