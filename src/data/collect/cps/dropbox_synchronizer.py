import dropbox
import shutil

from src.data.manager.config_manager import getConfig, setNewConfiguration, getTempConfigInfo
from src.data.manager.backup_manager import updateBackupDir
from src.share.trace import TRACE
from src.share.asserts import ASSERT_THROW

class DropboxSynchronizer:
    tempConfigPath = ''
    def __init__(self):
        downloadDropboxFile('config.json')
        tempConfigInfo = getTempConfigInfo()
        self.tempConfigPath = tempConfigInfo['tempConfigPath']
        onlineConfig = tempConfigInfo['tempConfig']

        self.onlineDate = onlineConfig['LAST_RECORD_DATE']
        self.onlineServicesHash = onlineConfig['SERVICES_HASH']

    def isDropboxSynchronizationNeeded(self):
        config = getConfig()
        currentDate = config['LAST_RECORD_DATE']
        currentServicesHash = config['SERVICES_HASH']

        if (currentDate != self.onlineDate):
            TRACE('DATES_MISMATCH -> DROPBOX_SYNCHRONIZATION_NEEDED')
            return True

        if (currentServicesHash != self.onlineServicesHash):
            TRACE('SERVICES_HASH_MISMATCH -> DROPBOX_SYNCHRONIZATION_NEEDED')
            return True

        return False

    def dropbboxSynchronization(self):
        setNewConfiguration(self.onlineDate,
                            self.onlineServicesHash)
        downloadDropboxFile('data.zip')
        removeExistingData()
        decompressData()
        updateBackupDir(self.tempConfigPath)
        TRACE('UPDATED BACKUP DIRECTORY FROM DROPBOX DATA')

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



    
