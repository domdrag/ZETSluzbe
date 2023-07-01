import dropbox
import ast

from src.data.share.utils.decompress_data import decompressData
from src.data.share.config_manager import getConfig, setConfig

RFRSH_TOKEN = 'wIxEqmHW0_IAAAAAAAAAAXS9N4JdzmOIt8rV90Y-uOVCdhhvC23S7qYHSSDSd53a'

def downloadData():
    dbx = dropbox.Dropbox(app_key = '9x72f19ngmg8mqo',
                          app_secret = 'msb8pniq2h76ym3',
                          oauth2_refresh_token = RFRSH_TOKEN)
    
    downloadComplete = False
    while not downloadComplete:
        try:
            dbx.files_download_to_file('data/dropbox/data.zip',
                                       '/data.zip')
            downloadComplete = True
        except:
            pass

def isDropboxSynchronizationNeeded():
    dbx = dropbox.Dropbox(app_key = '9x72f19ngmg8mqo',
                          app_secret = 'msb8pniq2h76ym3',
                          oauth2_refresh_token = RFRSH_TOKEN)
    
    downloadComplete = False
    while not downloadComplete:
        try:
            dbx.files_download_to_file('data/dropbox/last_record_date.txt',
                                       '/last_record_date.txt')
            downloadComplete = True
        except:
            pass

    config = getConfig()
    currentDate = config['LAST_RECORD_DATE']
    
    fileR = open('data/dropbox/last_record_date.txt', 'r')
    onlineDateString = fileR.read()
    onlineDate = ast.literal_eval(onlineDateString)
    fileR.close()

    if currentDate == oldDate:
        return False
    else:
        setConfig('LAST_RECORD_DATE', onlineDate)
        return True

def dropbboxSynchronization():
    downloadData()
    decompressData()





    
