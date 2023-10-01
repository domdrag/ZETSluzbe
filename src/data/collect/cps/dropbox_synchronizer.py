import dropbox
import shutil

from src.data.manager.config_manager import getConfig, setNewConfiguration, getTempConfig
from src.share.trace import TRACE
from src.share.asserts import ASSERT_THROW

class DropboxSynchronizer:
    def __init__(self):
        downloadDropboxFile('config.json')
        onlineConfig = getTempConfig()

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
            ASSERT_THROW(currentServicesHash == self.onlineServicesHash, 'Neuskladjene sluzbe sa dropbox-om.')
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
    config = getConfig()
    dbx = dropbox.Dropbox(app_key = config['DROPBOX_APP_KEY'],
                          app_secret = config['DROPBOX_APP_SECRET'],
                          oauth2_refresh_token = config['DROPBOX_REFRESH_TOKEN'])

    downloadComplete = False
    while not downloadComplete:
        try:
            dbx.files_download_to_file('data/temp/' + file,
                                       '/' + file)
            downloadComplete = True
        except:
            pass

def decompressData():
    shutil.unpack_archive('data/temp/data.zip', 'data/data')




    
