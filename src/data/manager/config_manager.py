import json

from functools import partial

from src.share.filenames import CONFIG_PATH

DATA_CORRUPTED = 1

class ConfigManager:
    _config = dict()

    @staticmethod
    def load():
        with open(CONFIG_PATH, 'r') as configFile:
            config = json.load(configFile)
        ConfigManager._config = config

    @staticmethod
    def getConfig(attributeName):
        return ConfigManager._config[attributeName]

    @staticmethod
    def dataCorrupted():
        return ConfigManager._config['DATA_CORRUPTED']

    @staticmethod
    def setNewDefaultOffNumAtStartup(newDefaultOffNum):
        ConfigManager._config['OFFICIAL_NUMBER_STARTUP'] = newDefaultOffNum
        with open(CONFIG_PATH, 'w', encoding='utf-8') as configFile:
            json.dump(ConfigManager._config, configFile, indent=3)

    @staticmethod
    def __setDataCorruptedFlag__(FLAG):
        ConfigManager._config['DATA_CORRUPTED'] = FLAG
        with open(CONFIG_PATH, 'w', encoding='utf-8') as configFile:
            json.dump(ConfigManager._config, configFile, indent=3)

    # aliases
    initiateDataUpdate = staticmethod(partial(__setDataCorruptedFlag__.__func__, DATA_CORRUPTED))
    initiateDataRecovery = staticmethod(partial(__setDataCorruptedFlag__.__func__, DATA_CORRUPTED))
    completeDataUpdate = staticmethod(partial(__setDataCorruptedFlag__.__func__, int(not DATA_CORRUPTED)))
    completeDataRecovery = staticmethod(partial(__setDataCorruptedFlag__.__func__, int(not DATA_CORRUPTED)))
