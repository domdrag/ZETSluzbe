import ast
import os
import zipfile

from src.data.collect.cps.utils.get_driver_info import getDriverInfo
from src.data.collect.cps.utils.get_service_layout import getServiceLayout
from src.data.collect.cps.utils.get_service_line import getServiceLine
from src.data.share.get_service_date import getServiceDate
from src.data.share.decompress_services import decompressShiftsFile
from src.share.filenames import (CENTRAL_DATA_DIR, COMPRESSED_SHIFTS_PATH, COMPRESSED_UPDATED_SHIFTS_PATH,
                                 WEEK_SERVICES_BY_DRIVER_ENCRYPTED_PATH, ALL_DRIVERS_PATH)

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
        shiftDate = getServiceDate(ast.literal_eval(shift[0]))
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

def compressShiftsFile(shiftsFile):
    with zipfile.ZipFile(COMPRESSED_UPDATED_SHIFTS_PATH,
                         'a',
                         zipfile.ZIP_DEFLATED) as updatedShiftsZIP:
        updatedShiftsZIP.write(CENTRAL_DATA_DIR + shiftsFile, shiftsFile)

def addOldShiftsWithNoUpdate():
    shiftsZIP = zipfile.ZipFile(COMPRESSED_SHIFTS_PATH, 'r', zipfile.ZIP_DEFLATED)
    updatedShiftsZIP = zipfile.ZipFile(COMPRESSED_UPDATED_SHIFTS_PATH, 'r', zipfile.ZIP_DEFLATED)
    shiftsWithNoUpdate = set(shiftsZIP.namelist()) - set(updatedShiftsZIP.namelist())
    for shiftsFile in shiftsWithNoUpdate:
        decompressShiftsFile(shiftsFile)
        compressShiftsFile(shiftsFile)
        os.remove(CENTRAL_DATA_DIR + shiftsFile)

def addDecryptedShifts(days,
                       weekSchedule,
                       mondayDate,
                       fileNames):
    zipfile.ZipFile(COMPRESSED_UPDATED_SHIFTS_PATH, 'w', zipfile.ZIP_DEFLATED)
    fileR = open(WEEK_SERVICES_BY_DRIVER_ENCRYPTED_PATH, 'r', encoding='utf-8')
    weekServicesALL = fileR.readlines()
    fileR.close()

    fileR = open(ALL_DRIVERS_PATH, 'r', encoding='utf-8')
    driversRaw = fileR.readlines()
    fileR.close()
    driverList = []
    for driverRaw in driversRaw:
        driver = driverRaw.split()
        driverList.append(driver)

    for weekServicesRaw in weekServicesALL:
        weekServices = ast.literal_eval(weekServicesRaw)
        offNum = int(weekServices[0])
        shiftsFile = str(offNum) + '.txt'
        decompressShiftsFile(shiftsFile)
        filePath = CENTRAL_DATA_DIR + shiftsFile
        newColleague = False

        if (os.path.isfile(filePath)):
            validOldShiftsIndexed = configureValidOldShiftsIndexed(filePath,
                                                                   mondayDate)
            numOfPreviouslyAddedShiftInsts = sum(len(shift) for shift in validOldShiftsIndexed if
                                               shift != None)
            if (numOfPreviouslyAddedShiftInsts):
                deletePreviouslyAddedShifts(filePath, numOfPreviouslyAddedShiftInsts)
            fileW = open(filePath, 'a', encoding='utf-8')
        else:
            newColleague = True
            fileW = open(filePath, 'w', encoding='utf-8')

        for i in range(1,8):
            if (not newColleague and validOldShiftsIndexed[i-1]):
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
        compressShiftsFile(shiftsFile)
        os.remove(filePath)

    addOldShiftsWithNoUpdate()
    os.remove(COMPRESSED_SHIFTS_PATH)
    os.rename(COMPRESSED_UPDATED_SHIFTS_PATH, COMPRESSED_SHIFTS_PATH)