import json

from src.data.manager.backup_manager import repairSystem
import src.share.trace as trace

CONFIG_FILE_PATH = 'data/config.json'
CURRENT_CONFIG = dict()

# called when:
# 1) app start
# 2) DataCollector fails
# 3) DataCollector begins in test configuration
def loadConfig():
    global CURRENT_CONFIG
    
    with open(CONFIG_FILE_PATH, 'r') as configFile:
        config = json.load(configFile)
    CURRENT_CONFIG = config

    # if some operation haven't stopped in the last session
    if (not CURRENT_CONFIG['UPDATE_SUCCESSFUL']):
        trace.TRACE('REPAIR ALL FILES - ERROR IN LAST SESSION')
        repairSystem()

def getConfig():
    return CURRENT_CONFIG

# configure setConfig so the caller doesn't need to know what values should he send
# for example: caller might send True/False, but we need to set that to 1/0
def setConfig(configName, configValue):
    CURRENT_CONFIG[configName] = configValue
    with open(CONFIG_FILE_PATH, 'w') as configFile:
        json.dump(CURRENT_CONFIG, configFile, indent = 2)

def setNewConfiguration(mondayDateList, missingServices, servicesHash):
    setConfig('LAST_RECORD_DATE', mondayDateList)
    setConfig('MISSING_SERVICES', missingServices)
    setConfig('SERVICES_HASH', servicesHash)

#################################################################

TEMP_CONFIG_COPY_FILE_PATH = 'data/temp/config.json'

def getTempConfigInfo():
    with open(TEMP_CONFIG_COPY_FILE_PATH, 'r') as configFile:
        tempConfig = json.load(configFile)

    return {'tempConfig': tempConfig, 'tempConfigPath': TEMP_CONFIG_COPY_FILE_PATH}

def setTempConfig(tempConfig):
    with open(TEMP_CONFIG_COPY_FILE_PATH, 'w') as configFile:
        json.dump(tempConfig, configFile, indent = 3)