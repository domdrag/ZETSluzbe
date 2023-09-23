import dropbox

from src.data.manager.config_manager import getConfig
from src.share.trace import TRACE

def uploadDataToDropbox():
    config = getConfig()
    dbx = dropbox.Dropbox(app_key = config['DROPBOX_APP_KEY'],
                          app_secret = config['DROPBOX_APP_SECRET'],
                          oauth2_refresh_token = config['DROPBOX_REFRESH_TOKEN'])
    # WORKAROUND - connection fails on PC during uploads for some reason
    dataSent = False
    while not dataSent:
        try:
            with open('./data/temp/data.zip', 'rb') as f:
                dbx.files_upload(f.read(),
                                 '/data.zip',
                                 mode=dropbox.files.WriteMode.overwrite)
            dataSent = True
        except:
            TRACE(e)

    configSent = False
    while not configSent:
        try:
            with open('./data/temp/config.json', 'rb') as f:
                dbx.files_upload(f.read(),
                                 '/config.json',
                                 mode=dropbox.files.WriteMode.overwrite)
            configSent = True
        except:
            TRACE(e)
