import dropbox
import ast
import json
import shutil

from src.data.share.config_manager import getConfig, setConfig
from src.share.trace import TRACE

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
def isDropboxSynchronizationNeeded():
    dbx = dropbox.Dropbox(app_key = '9x72f19ngmg8mqo',
                          app_secret = 'msb8pniq2h76ym3',
                          oauth2_refresh_token = RFRSH_TOKEN)

    downloadDropboxFile('config.json')
    onlineConfig = getOnlineConfig()
    onlineDate = onlineConfig['LAST_RECORD_DATE']

    config = getConfig()
    currentDate = config['LAST_RECORD_DATE']

    if currentDate == onlineDate:
        TRACE('DROPBOX_SYNCHRONIZATION_NOT_NEEDED')
        return False
    else:
        setConfig('LAST_RECORD_DATE', onlineDate)
        # relevant for admin only
        setConfig('MISSING_SERVICES', onlineConfig['MISSING_SERVICES'])
        return True

def dropbboxSynchronization():
    downloadDropboxFile('data.zip')
    decompressData()





    
