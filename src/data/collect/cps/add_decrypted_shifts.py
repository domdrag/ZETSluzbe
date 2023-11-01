import ast

from src.data.collect.cps.utils.get_driver_info import (
    getDriverInfo
    )
from src.data.collect.cps.utils.get_service_layout import getServiceLayout
from src.data.collect.cps.utils.get_service_line import getServiceLine
from src.data.collect.cps.utils.count_previously_added_services import countPreviouslyAddedServices
from src.data.manager.config_manager import getConfig

def configureEmptyShifts():
    return [None] * 7

def getValidOldShiftsUnordered(filePath, numOfPreviouslyAddedServices):
    fileR = open(filePath, 'r', encoding='utf-8')
    shifts = fileR.readlines()
    fileR.close()

    validOldShiftsUnordered = []
    numOfShifts = len(shifts)
    currentIndex = numOfShifts - 1
    # REMARK: assumed currentIndex >> 0
    while(numOfPreviouslyAddedServices):
        numOfPreviouslyAddedServices = numOfPreviouslyAddedServices - 1
        shiftInst = shifts[currentIndex]
        shiftInstBefore = shifts[currentIndex-1]
        if (ast.literal_eval(shiftInst)[0] == ast.literal_eval(shiftInstBefore)[0]):
            shiftInstBeforeBefore = shifts[currentIndex-2]
            validOldShiftsUnordered.append([shiftInstBeforeBefore, shiftInstBefore, shiftInst])
            currentIndex = currentIndex - 3
        else:
            validOldShiftsUnordered.append([shiftInst])
            currentIndex = currentIndex - 1

    return validOldShiftsUnordered[::-1]

def configureValidOldIndexedShifts(filePath, oldMissingServices, numOfPreviouslyAddedServices):
    fileR = open(filePath, 'r', encoding='utf-8')
    shifts = fileR.readlines()
    fileR.close()

    validOldShifts = configureEmptyShifts()
    validOldShiftsUnordered = getValidOldShiftsUnordered(filePath, numOfPreviouslyAddedServices)
    currValidOldShiftIndex = 0
    for i in range(len(oldMissingServices)):
        if (not oldMissingServices[i]):
            validOldShifts[i] = validOldShiftsUnordered[currValidOldShiftIndex]
            currValidOldShiftIndex = currValidOldShiftIndex + 1

    numOfPreviouslyAddedShifts = sum([len(shift) for shift in validOldShiftsUnordered])
    return {'validOldIndexedShifts': validOldShifts,
            'numOfPreviouslyAddedShifts': numOfPreviouslyAddedShifts}
def deletePreviouslyAddedShifts(filePath, numOfPreviouslyAddedShifts):
    fileR = open(filePath, 'r', encoding='utf-8')
    shifts = fileR.readlines()
    fileR.close()

    numOfShifts = len(shifts)
    numOfKeptShifts = numOfShifts - numOfPreviouslyAddedShifts

    fileW = open(filePath, 'w', encoding='utf-8')
    for i in range(numOfKeptShifts):
        fileW.write(shifts[i])
    fileW.close()
def addDecryptedShifts(days,
                       weekSchedule,
                       missingServices,
                       updateCause,
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
        filePath = 'data/data/all_shifts_by_driver_decrypted/' \
                    + str(offNum) \
                    + '.txt'
        if (updateCause == 'MISSING_SERVICES'):
            config = getConfig()
            oldMissingServices = config['MISSING_SERVICES']
            numOfPreviouslyAddedServices = countPreviouslyAddedServices(oldMissingServices)
            result = configureValidOldIndexedShifts(filePath,
                                                    oldMissingServices,
                                                    numOfPreviouslyAddedServices)
            validOldIndexedShifts = result['validOldIndexedShifts']
            numOfPreviouslyAddedShifts = result['numOfPreviouslyAddedShifts']
            deletePreviouslyAddedShifts(filePath, numOfPreviouslyAddedShifts)
        else:
            validOldIndexedShifts = configureEmptyShifts()

        fileW = open(filePath, 'a', encoding='utf-8')
        for i in range(1,8):
            if (validOldIndexedShifts[i-1]):
                validOldShift = validOldIndexedShifts[i-1]
                for shiftInstance in validOldShift:
                    # already contains newline
                    fileW.write(shiftInstance)
                continue
            if (missingServices[i-1]):
                continue

            serviceNum = weekServices[i]
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