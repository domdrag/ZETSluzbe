import json

LAST_UPDATE_INFO_FILE_PATH = 'data/data/last_update_info.json'

class UpdateInfoManager:
    __lastUpdateInfo__ = dict()
    __currentUpdateInfo__ = dict()

    @staticmethod
    def load():
        with open(LAST_UPDATE_INFO_FILE_PATH, 'r', encoding='utf-8') as lastUpdateInfoFile:
            UpdateInfoManager.__lastUpdateInfo__ = json.load(lastUpdateInfoFile)

    @staticmethod
    def getUpdateInfo(attributeName):
        if attributeName.startswith('LAST'):
            return UpdateInfoManager.__lastUpdateInfo__[attributeName]
        else:
            return UpdateInfoManager.__currentUpdateInfo__[attributeName]

