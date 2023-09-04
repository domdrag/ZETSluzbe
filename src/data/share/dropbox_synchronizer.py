import dropbox
import ast
import json
import shutil

from src.data.share.config_manager import getConfig, setConfig, setNewConfiguration
from src.share.trace import TRACE

RFRSH_TOKEN = 'wIxEqmHW0_IAAAAAAAAAAXS9N4JdzmOIt8rV90Y-uOVCdhhvC23S7qYHSSDSd53a'

class DropboxSynchronizer:
    def __init__(self):
        downloadDropboxFile('config.json')
        onlineConfig = getOnlineConfig()

        self.onlineDate = onlineConfig['LAST_RECORD_DATE']
        self.onlineMissingServices = onlineConfig['MISSING_SERVICES']
        self.onlineServicesHash = onlineConfig['SERVICES_HASH']

    def isDropboxSynchronizationNeeded(self):
        config = getConfig()
        currentDate = config['LAST_RECORD_DATE']
        currentMissingServices = config['MISSING_SERVICES']
        currentServicesHash = config['SERVICES_HASH']

        if (currentDate != self.onlineDate):
            TRACE('DATES_MISMATCH -> DROPBOX_SYNCHRONIZATION_NEEDED')
            return True
        elif (currentMissingServices != self.onlineMissingServices):
            TRACE('MISSING_SERVICES_MISMATCH -> DROPBOX_SYNCHRONIZATION_NEEDED')
            return True
        else:
            TRACE('DROPBOX_SYNCHRONIZATION_NOT_NEEDED')
            assert currentServicesHash == self.onlineServicesHash, 'Neuskladjene sluzbe sa dropbox-om.'
            return False

    def dropbboxSynchronization(self):
        setNewConfiguration(self.onlineDate,
                            self.onlineMissingServices,
                            self.onlineServicesHash)
        downloadDropboxFile('data.zip')
        removeExistingData()
        decompressData()

###########################################################################################
###########################################################################################

def removeExistingData():
    # remove complete directory
    shutil.rmtree('data/data')

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

def decompressData():
    shutil.unpack_archive('data/dropbox/data.zip', 'data/data')

def getOnlineConfig():
    with open('data/dropbox/config.json', 'r') as configFile:
        onlineConfig = json.load(configFile)

    return onlineConfig




    
