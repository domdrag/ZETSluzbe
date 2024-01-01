from datetime import date

from src.data.manager.update_info_manager import UpdateInfoManager
from src.share.trace import TRACE

def checkUpdateNeeded(mondayDate, servicesHash):
    lastRecordedMondayDateList = UpdateInfoManager.getUpdateInfo('LAST_RECORDED_MONDAY_DATE')
    lastRecordedMondayDate = date(lastRecordedMondayDateList[0],
                          lastRecordedMondayDateList[1],
                          lastRecordedMondayDateList[2])

    if (mondayDate != lastRecordedMondayDate):
        TRACE('MONDAY_ZET_ONLINE_DIFFERENT_FROM_LAST_RECORDED_MONDAY -> UPDATE_NEEDED')
        return True

    lastServicesHash = UpdateInfoManager.getUpdateInfo('SERVICES_HASH')
    TRACE('LAST_SERVICES_HASH: ' + str(lastServicesHash))
    TRACE('NEW_SERVICES_HASH: ' + str(servicesHash))
    if (lastServicesHash != servicesHash):
        # for what I know, this should only be the case if there were missing services beforehand
        # -> client code depends on that knowledge
        TRACE('SERVICES_HASH_DIFFERENCE -> UPDATE_NEEDED')
        return True

    TRACE('NO_UPDATE_NEEDED')
    return False