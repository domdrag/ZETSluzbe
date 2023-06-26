import json

def getConfig():
    with open('data/config/config.json', 'r') as configFile:
        config = json.load(configFile)
    return config

