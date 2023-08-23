import dropbox
import ast
import json
import shutil

from src.data.share.config_manager import getConfig, setConfig
from src.share.trace import TRACE
from src.data.share.set_new_config import setNewConfig

RFRSH_TOKEN = 'wIxEqmHW0_IAAAAAAAAAAXS9N4JdzmOIt8rV90Y-uOVCdhhvC23S7qYHSSDSd53a'

def decompressData():
    shutil.unpack_archive('data/dropbox/data.zip', 'data/data')
def downloadDropboxFile(file):
    dbx = dropbox.Dropbox(app_key='9x72f19ngmg8mqo',
                          app_secret='msb8pniq2h76ym3',
                          oauth2_refresh_token=RFRSH_TOKEN)

    downloadComplete = False
    while not downloadComplete:
        try:
            dbx.files_download_to_file('data/dropbox/' + file,
                                       '/' + file)
            downloadComplete = True
        except:
            pass

def getOnlineConfig():
    with open('data/dropbox/config.json', 'r') as configFile:
        onlineConfig = json.load(configFile)

    return onlineConfig

###########################################################################

def determineDropboxSyncNeeded(currentDate,
                               onlineDate,
                               currentMissingServices,
                               onlineMissingServices):
    if (currentDate != onlineDate):
        TRACE('DATES_MISMATCH -> DROPBOX_SYNCHRONIZATION_NEEDED')
        return True
    elif (currentMissingServices != onlineMissingServices):
        TRACE('MISSING_SERVICES_MISMATCH -> DROPBOX_SYNCHRONIZATION_NEEDED')
        return True
    else:
        return False

def isDropboxSynchronizationNeeded():
    dbx = dropbox.Dropbox(app_key = '9x72f19ngmg8mqo',
                          app_secret = 'msb8pniq2h76ym3',
                          oauth2_refresh_token = RFRSH_TOKEN)

    downloadDropboxFile('config.json')
    onlineConfig = getOnlineConfig()
    onlineDate = onlineConfig['LAST_RECORD_DATE']
    onlineMissingServices = onlineConfig['MISSING_SERVICES']
    onlineServicesHash = onlineConfig['SERVICES_HASH']

    config = getConfig()
    currentDate = config['LAST_RECORD_DATE']
    currentMissingServices = config['MISSING_SERVICES']
    currentServicesHash = config['SERVICES_HASH']

    if (determineDropboxSyncNeeded(currentDate,
                                   onlineDate,
                                   currentMissingServices,
                                   onlineMissingServices)):
        setNewConfig(onlineDate, onlineMissingServices, onlineServicesHash)
        return True
    else:
        TRACE('DROPBOX_SYNCHRONIZATION_NOT_NEEDED')
        assert currentServicesHash == onlineServicesHash, 'Neuskladjene sluzbe sa dropbox-om.'
        return False

def dropbboxSynchronization():
    downloadDropboxFile('data.zip')
    decompressData()





    
