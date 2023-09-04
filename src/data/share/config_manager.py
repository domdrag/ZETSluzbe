import json

from src.data.share.backup_manager import repairAllFiles
import src.share.trace as trace

CONFIG_FILE_PATH = 'data/config.json'
CURRENT_CONFIG = dict()

# called by the app at the start
def loadConfig():
    global CURRENT_CONFIG
    
    with open(CONFIG_FILE_PATH, 'r') as configFile:
        config = json.load(configFile)
    CURRENT_CONFIG = config

    # if some operation haven't stopped in last session
    if (not CURRENT_CONFIG['UPDATE_SUCCESSFUL']):
        trace.TRACE('REPAIR ALL FILES - ERROR IN LAST SESSION')
        repairAllFiles()
        loadConfig()

def getConfig():
    return CURRENT_CONFIG

# configure setConfig so the caller doesn't need to know what values should he send
# for example: caller might send True/False, but we need to set that to 1/0
def setConfig(configName, configValue):
    CURRENT_CONFIG[configName] = configValue
    with open(CONFIG_FILE_PATH, 'w') as configFile:
        json.dump(CURRENT_CONFIG, configFile, indent = 3)

def setNewConfiguration(mondayDateList, missingServices, servicesHash):
    setConfig('LAST_RECORD_DATE', mondayDateList)
    setConfig('MISSING_SERVICES', missingServices)
    setConfig('SERVICES_HASH', servicesHash)
