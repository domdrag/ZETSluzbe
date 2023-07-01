import json

def getConfig():
    with open('data/config/config.json', 'r') as configFile:
        config = json.load(configFile)
    return config

def setConfig(configName, configValue):
    config = getConfig()

    config[configName] = configValue
    with open('data/config/config.json', 'w') as configFile:
        json.dump(config, configFile, indent = 3)
