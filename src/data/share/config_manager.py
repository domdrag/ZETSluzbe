import json

CURRENT_CONFIG = dict()

# called by the app at the start
def loadConfig():
    global CURRENT_CONFIG
    
    with open('data/config.json', 'r') as configFile:
        config = json.load(configFile)

    if (config['UPDATE_SUCCESSFUL']):
        CURRENT_CONFIG = config
        
    else: # if some operation haven't stopped in last session
        # can't use trace.py because of circularity
        print('REPAIR ALL FILES - ERROR IN LAST SESSION')
        repairAllFiles()
        loadConfig()

def getConfig():
    return CURRENT_CONFIG

def setConfig(configName, configValue):
    CURRENT_CONFIG[configName] = configValue
    with open('data/config.json', 'w') as configFile:
        json.dump(CURRENT_CONFIG, configFile, indent = 3)
