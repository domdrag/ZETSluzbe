import shutil
import json

DROPBOX_CONFIG_COPY_FILE_PATH = 'data/dropbox/config.json'
def compressData():
    shutil.make_archive('data/dropbox/data', 'zip', 'data/data')

def setUpdateSuccessfulForDropboxUpload():
    with open(DROPBOX_CONFIG_COPY_FILE_PATH, 'r') as configFile:
        configCopy = json.load(configFile)
    configCopy['UPDATE_SUCCESSFUL'] = 1
    with open(DROPBOX_CONFIG_COPY_FILE_PATH, 'w') as configFile:
        json.dump(configCopy, configFile, indent = 3)

def prepareDataForTransport():
    compressData()
    shutil.copyfile('data/config.json', 'data/dropbox/config.json')
    setUpdateSuccessfulForDropboxUpload()