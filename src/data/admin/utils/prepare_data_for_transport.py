import shutil
import json

TEMP_CONFIG_COPY_FILE_PATH = 'data/temp/config.json'
def compressData():
    shutil.make_archive('data/temp/data', 'zip', 'data/data')

def setUpdateSuccessfulForUpload():
    with open(TEMP_CONFIG_COPY_FILE_PATH, 'r') as configFile:
        configCopy = json.load(configFile)
    configCopy['UPDATE_SUCCESSFUL'] = 1
    with open(TEMP_CONFIG_COPY_FILE_PATH, 'w') as configFile:
        json.dump(configCopy, configFile, indent = 3)

def prepareDataForTransport():
    compressData()
    shutil.copyfile('data/config.json', 'data/temp/config.json')
    setUpdateSuccessfulForUpload()