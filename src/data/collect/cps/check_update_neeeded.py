from datetime import date

from src.data.manager.update_info_manager import UpdateInfoManager
from src.share.trace import TRACE

def checkUpdateNeeded(mondayDate, servicesHash):
    lastRecordDateList = UpdateInfoManager.getUpdateInfo('LAST_RECORD_DATE')
    lastRecordDate = date(lastRecordDateList[0],
                          lastRecordDateList[1],
                          lastRecordDateList[2])

    if (mondayDate != lastRecordDate):
        TRACE('MONDAY_ZET_ONLINE_DIFFERENT_FROM_LAST_RECORDED_MONDAY -> UPDATE_NEEDED')
        return True

    lastServicesHash = UpdateInfoManager.getUpdateInfo('LAST_SERVICES_HASH')
    TRACE('LAST_SERVICES_HASH: ' + str(lastServicesHash))
    TRACE('NEW_SERVICES_HASH: ' + str(servicesHash))
    if (lastServicesHash != servicesHash):
        TRACE('SERVICES_HASH_DIFFERENCE -> UPDATE_NEEDED')
        return True

    TRACE('NO_UPDATE_NEEDED')
    return False