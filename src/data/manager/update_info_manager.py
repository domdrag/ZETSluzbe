import json

from src.share.filenames import UPDATE_INFO_PATH, DOWNLOADED_UPDATE_INFO_PATH

class UpdateInfoManager:
    __updateInfo__ = dict()
    __dataUpdated__ = False

    @staticmethod
    def load():
        with open(UPDATE_INFO_PATH, 'r', encoding='utf-8') as updateInfoFile:
            UpdateInfoManager.__updateInfo__ = json.load(updateInfoFile)
        UpdateInfoManager.__dataUpdated__ = False

    @staticmethod
    def getUpdateInfo(attributeName):
        return UpdateInfoManager.__updateInfo__[attributeName]

    @staticmethod
    def getDownloadedUpdateInfo(attributeName):
        with open(DOWNLOADED_UPDATE_INFO_PATH, 'r', encoding='utf-8') as updateInfoFile:
            updateInfo = json.load(updateInfoFile)
        return updateInfo[attributeName]

    @staticmethod
    def pushNewUpdateInfo(newRecordDate, newServicesHash, newMissingServices):
        UpdateInfoManager.__updateInfo__['LAST_RECORDED_MONDAY_DATE'] = newRecordDate
        UpdateInfoManager.__updateInfo__['MISSING_SERVICES'] = int(newMissingServices)
        UpdateInfoManager.__updateInfo__['SERVICES_HASH'] = newServicesHash

        with open(UPDATE_INFO_PATH, 'w', encoding='utf-8') as updateInfoFile:
            json.dump(UpdateInfoManager.__updateInfo__, updateInfoFile, indent=3)

    @staticmethod
    def isDataUpdated():
        return UpdateInfoManager.__dataUpdated__

    @staticmethod
    def setDataUpdated():
        UpdateInfoManager.__dataUpdated__ = True

