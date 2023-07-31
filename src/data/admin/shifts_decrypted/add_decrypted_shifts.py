import ast

from src.data.admin.shifts_decrypted.utils.get_driver_info import (
    getDriverInfo
    )
from src.data.admin.utils.get_service_layout import getServiceLayout
from src.data.admin.utils.get_service_line import getServiceLine
from src.data.share.config_manager import getConfig

def deletePreviouslyAddedShifts(filePath, numOfPreviouslyAddedServices):
    fileR = open(filePath, 'r', encoding='utf-8')
    shifts = fileR.readlines()
    fileR.close()

    numOfShifts = len(shifts)
    numOfKeptShifts = numOfShifts
    currentIndex = numOfShifts - 1
    # REMARK: assumed currentIndex >> 0
    while(numOfPreviouslyAddedServices):
        numOfPreviouslyAddedServices = numOfPreviouslyAddedServices - 1
        shift = ast.literal_eval(shifts[currentIndex])
        shiftBefore = ast.literal_eval(shifts[currentIndex-1])
        if (shift[0] == shiftBefore[0]):
            numOfKeptShifts = numOfKeptShifts - 3
            currentIndex = currentIndex - 3
        else:
            numOfKeptShifts = numOfKeptShifts - 1
            currentIndex = currentIndex - 1

    fileW = open(filePath, 'w', encoding='utf-8')
    for i in range(numOfKeptShifts):
        fileW.write(shifts[i])
    fileW.close()
def addDecryptedShifts(days, weekSchedule, numOfPreviouslyAddedServices = None):
    fileR = open('data/data/week_services_by_driver_encrypted.txt',
                 'r',
                 encoding='utf-8')
    weekServicesALL = fileR.readlines()
    fileR.close()

    fileR = open('data/data/all_drivers.txt', 'r', encoding='utf-8')
    driversRaw = fileR.readlines()
    fileR.close()
    driverList = []
    for driverRaw in driversRaw:
        driver = driverRaw.split()
        driverList.append(driver)

    config = getConfig()
    missingServices = config['MISSING_SERVICES']
    for weekServicesRaw in weekServicesALL:
        weekServices = ast.literal_eval(weekServicesRaw)
        offNum = int(weekServices[0])
        filePath = 'data/data/all_shifts_by_driver_decrypted/' \
                    + str(offNum) \
                    + '.txt'
        if (numOfPreviouslyAddedServices):
            deletePreviouslyAddedShifts(filePath, numOfPreviouslyAddedServices)

        fileW = open(filePath, 'a', encoding='utf-8')        
        for i in range(1,8):
            if (missingServices[i-1]):
                continue

            serviceNum = weekServices[i]
            serviceLine = getServiceLine(serviceNum, i-1, weekSchedule)
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

def addMissingDecryptedShifts(days, weekSchedule, numOfPreviouslyAddedServices):
    addDecryptedShifts(days, weekSchedule, numOfPreviouslyAddedServices)