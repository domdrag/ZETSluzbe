import os
import shutil
import json
import zipfile

def setTestConfiguration(configPath, testPackNum):
    with open(configPath, 'r') as configFile:
        config = json.load(configFile)

    config['ACTIVATED_TEST_PACK_NUM'] = testPackNum

    with open(configPath, 'w') as configFile:
        json.dump(config, configFile, indent = 3)

def fixNotificationURLs(notificationsPath, testPackNum):
    with open(notificationsPath, 'r') as notificationsFile:
        notifications = json.load(notificationsFile)

    for notificationInfo in notifications.values():
        oldDomain = 'www.zet.hr'
        newDomainWithPath = 'domdrag.github.io/test_pack_' + str(testPackNum)
        newInfo = notificationInfo['URL'].replace(oldDomain, newDomainWithPath)
        notificationInfo['URL'] = newInfo
                                            
    with open(notificationsPath, 'w') as notificationsFile:
        json.dump(notifications, notificationsFile, indent = 3)

def setupDataDirectory():
    shutil.copytree('backup_original_data/backup', 'data/backup')
    shutil.copytree('backup_original_data/data', 'data/data')

    files = os.listdir('backup_original_data')
    for file in files:
        if (os.path.isfile('backup_original_data/' + file)):
            shutil.copyfile('backup_original_data/' + file,
                            'data/' + file)
    
def fixData():
    print('FIXING TEST DATA')
    currentDir = os.getcwd()
    if (currentDir[-2:].isnumeric()):
        testPackNum = int(currentDir[-2:])
    else:
        testPackNum = int(currentDir[-1])
    
    setTestConfiguration('backup_original_data/config.json',
                         testPackNum)
    setTestConfiguration('wanted_data/config.json',
                         testPackNum)

    fixNotificationURLs('wanted_data/central_data/notifications.json',
                        testPackNum)
    
    if (os.path.isdir('ZETSluzbe-Data')):
        shutil.rmtree('ZETSluzbe-Data')
    shutil.copytree('backup_original_data', 'ZETSluzbe-Data/data')

def fixCollectedData():
    unpackedServicesPath = 'ZETSluzbe-Data/data/central_data/services'
    unpackedShiftsPath = 'ZETSluzbe-Data/data/central_data/shifts'
    with zipfile.ZipFile('ZETSluzbe-Data/data/central_data/services.zip',
                         'r',
                         zipfile.ZIP_DEFLATED) as servicesZip:
        servicesZip.extractall(unpackedServicesPath)

    with zipfile.ZipFile('ZETSluzbe-Data/data/central_data/shifts.zip',
                         'r',
                         zipfile.ZIP_DEFLATED) as shiftsZip:
        shiftsZip.extractall(unpackedShiftsPath)
        
    os.remove('ZETSluzbe-Data/data/central_data/services.zip')
    os.remove('ZETSluzbe-Data/data/central_data/shifts.zip')


        

    
