import ast

from src.share.filenames import WEEK_SERVICES_BY_DRIVER_ENCRYPTED_PATH

def getDriverInfo(serviceNum, driverList, day, testConfig):
    fileR = open(WEEK_SERVICES_BY_DRIVER_ENCRYPTED_PATH, 'r', encoding='utf-8')
    weekServicesALL = fileR.readlines()
    fileR.close()
    wantedOffNum = -1
    for weekServicesRaw in weekServicesALL:
        weekServices = ast.literal_eval(weekServicesRaw)
        if(weekServices[day] == serviceNum):
            wantedOffNum = int(weekServices[0])
            break
        
    if(wantedOffNum == -1):
        return ['ANON', 'XXX-XXX-XXXX']

    for driver in driverList:
        if (driver[0] != str(wantedOffNum)):
            continue
        if (testConfig):
            driverName = driver[1] + ' ' + driver[2][:-1]
            telNum = driver[3]
            driverTelNumber = f"{telNum[:3]}-{telNum[3:6]}-{telNum[6:]}"
        else:
            driverName = driver[1] + ' ' + driver[2]
            driverTelNumber = driver[3]
        return [driverName, driverTelNumber]
    return ['ANON', 'XXX-XXX-XXXX']
