import json

UPDATE_INFO_FILE_PATH = 'data/central_data/update_info.json'

class UpdateInfoManager:
    __updateInfo__ = dict()
    __dataUpdated__ = False

    @staticmethod
    def load():
        with open(UPDATE_INFO_FILE_PATH, 'r', encoding='utf-8') as updateInfoFile:
            UpdateInfoManager.__updateInfo__ = json.load(updateInfoFile)
        UpdateInfoManager.__dataUpdated__ = False

    @staticmethod
    def getUpdateInfo(attributeName):
        return UpdateInfoManager.__updateInfo__[attributeName]

    @staticmethod
    def pushNewUpdateInfo(newRecordDate, newServicesHash):
        UpdateInfoManager.setDataUpdated()
        UpdateInfoManager.__updateInfo__['RECORD_DATE'] = newRecordDate
        UpdateInfoManager.__updateInfo__['SERVICES_HASH'] = newServicesHash

        with open(UPDATE_INFO_FILE_PATH, 'w', encoding='utf-8') as updateInfoFile:
            json.dump(UpdateInfoManager.__updateInfo__, updateInfoFile, indent=3)

    @staticmethod
    def isDataUpdated():
        return UpdateInfoManager.__dataUpdated__

    @staticmethod
    def setDataUpdated():
        UpdateInfoManager.__dataUpdated__ = True

