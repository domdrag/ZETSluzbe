import dropbox
import shutil

from src.data.manager.config_manager import ConfigManager
from src.data.manager.backup_manager import updateBackupDir
from src.share.trace import TRACE
from src.share.asserts import ASSERT_THROW

class DropboxSynchronizer:
    def __init__(self):
        downloadDropboxFile('config.json')
        self.onlineLastRecordDate = ConfigManager.getTempConfig('LAST_RECORD_DATE')
        self.onlineServicesHash = ConfigManager.getTempConfig('SERVICES_HASH')

    def isDropboxSynchronizationNeeded(self):
        currentDate = ConfigManager.getConfig('LAST_RECORD_DATE')
        currentServicesHash = ConfigManager.getConfig('SERVICES_HASH')

        if (currentDate != self.onlineLastRecordDate):
            TRACE('DATES_MISMATCH -> DROPBOX_SYNCHRONIZATION_NEEDED')
            return True

        if (currentServicesHash != self.onlineServicesHash):
            TRACE('SERVICES_HASH_MISMATCH -> DROPBOX_SYNCHRONIZATION_NEEDED')
            return True

        return False

    def dropbboxSynchronization(self):
        # During update, synced data acts like current data
        ConfigManager.updateConfig('LAST_RECORD_DATE', self.onlineLastRecordDate)
        ConfigManager.updateConfig('SERVICES_HASH', self.onlineServicesHash)
        downloadDropboxFile('data.zip')
        removeExistingData()
        decompressData()
        TRACE('UPDATED BACKUP DIRECTORY FROM DROPBOX DATA')

###########################################################################################
###########################################################################################

def removeExistingData():
    # remove complete directory
    shutil.rmtree('data/data')

def downloadDropboxFile(file):
    dbx = dropbox.Dropbox(app_key = ConfigManager.getConfig('DROPBOX_APP_KEY'),
                          app_secret = ConfigManager.getConfig('DROPBOX_APP_SECRET'),
                          oauth2_refresh_token = ConfigManager.getConfig('DROPBOX_REFRESH_TOKEN'))

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



    
