import json
import copy
import shutil

import src.share.trace as trace
from src.share.asserts import ASSERT_THROW

CONFIG_FILE_PATH = 'data/config.json'
BACKUP_CONFIG_FILE_PATH = 'data/backup/config.json'
TEMP_CONFIG_COPY_FILE_PATH = 'data/temp/config.json'
UPDATE_UNSUCCESSFUL = 0
UPDATE_SUCCESSFUL = 1

class ConfigManager:
    __currentConfig__ = dict()
    __updatedConfig__ = dict()
    __isUpdateOngoing__ = False

    @staticmethod
    def load():
        with open(CONFIG_FILE_PATH, 'r') as configFile:
            config = json.load(configFile)
        ConfigManager.__currentConfig__ = config

    @staticmethod
    def initializeUpdate():
        if (not ConfigManager.__currentConfig__):
            ConfigManager.load() # verification purposes

        # need to mark the flag for failure detection
        #ConfigManager.markUpdateSuccessfulFlag(UPDATE_UNSUCCESSFUL)

        ConfigManager.__isUpdateOngoing__ = True
        ConfigManager.__updatedConfig__ = copy.deepcopy(ConfigManager.__currentConfig__)

    @staticmethod
    def getConfig(attributeName):
        # Dropbox sync CP may changed the config so we want to return updated one
        ## since synced data is acting like current data during update
        if (ConfigManager.__isUpdateOngoing__):
            return ConfigManager.__updatedConfig__[attributeName]
        else:
            return ConfigManager.__currentConfig__[attributeName]

    @staticmethod
    def finishUpdate():
        ConfigManager.__currentConfig__ = copy.deepcopy(ConfigManager.__updatedConfig__)
        ConfigManager.abandonUpdate()

    @staticmethod
    # Common method for both success and failure update; in both cases pushes config
    # If success, currentConfig will become updatedConfig; otherwise no new changes pushed
    def abandonUpdate():
        ConfigManager.__isUpdateOngoing__ = False
        ConfigManager.markUpdateSuccessfulFlag(UPDATE_SUCCESSFUL)

    @staticmethod
    def markUpdateSuccessfulFlag(flag):
        ASSERT_THROW(not ConfigManager.__isUpdateOngoing__,
                     'ERROR - MARKING UPDATE SUCCESS FLAG WHILE UPDATING')
        ConfigManager.updateConfig('UPDATE_SUCCESSFUL', flag)

    @staticmethod
    def updateConfig(attributeName, attributeValue):
        # if updating config while no update in ongoing, push the new updates immediately
        if (ConfigManager.__isUpdateOngoing__):
            ConfigManager.__updatedConfig__[attributeName] = attributeValue
        else:
            ConfigManager.__currentConfig__[attributeName] = attributeValue
            ConfigManager.pushNewUpdate()

    @staticmethod
    def pushNewUpdate():
        ASSERT_THROW(not ConfigManager.__isUpdateOngoing__,
                     'ERROR - PUSHING NEW CONFIG WHILE UPDATING')
        with open(CONFIG_FILE_PATH, 'w', encoding='utf-8') as configFile:
            json.dump(ConfigManager.__currentConfig__, configFile, indent=3)

    @staticmethod
    def updateBackupConfig():
        shutil.copyfile(CONFIG_FILE_PATH, BACKUP_CONFIG_FILE_PATH)

    @staticmethod
    def recoverConfig():
        shutil.copyfile(BACKUP_CONFIG_FILE_PATH, CONFIG_FILE_PATH)

    @staticmethod
    def prepareConfigForForcedSystemExit():
        ConfigManager.updateConfig('UPDATE_SUCCESSFUL', UPDATE_UNSUCCESSFUL)

    @staticmethod
    def getFullConfigString():
        return str(ConfigManager.__currentConfig__).replace(',', ',\n')

    ##################################################################################
    ########################### TEMP CONFIG METHODS ##################################
    ##################################################################################
    @staticmethod
    def getTempConfig(attributeName):
        with open(TEMP_CONFIG_COPY_FILE_PATH, 'r') as configFile:
            tempConfig = json.load(configFile)
        return tempConfig[attributeName]

    @staticmethod
    def prepareConfigToTransport():
        configToTransport = copy.deepcopy(ConfigManager.__updatedConfig__)
        configToTransport['UPDATE_SUCCESSFUL'] = UPDATE_SUCCESSFUL
        with open(TEMP_CONFIG_COPY_FILE_PATH, 'w') as configFile:
            json.dump(configToTransport, configFile, indent=3)