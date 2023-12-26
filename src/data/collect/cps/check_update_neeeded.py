from datetime import date

from src.data.manager.config_manager import ConfigManager
from src.share.trace import TRACE

def checkUpdateNeeded(mondayDate, servicesHash):
    lastRecordDateConfig = ConfigManager.getConfig('LAST_RECORD_DATE')
    lastRecordDate = date(lastRecordDateConfig[0],
                          lastRecordDateConfig[1],
                          lastRecordDateConfig[2])

    if (mondayDate != lastRecordDate):
        TRACE('MONDAY_ZET_ONLINE_DIFFERENT_FROM_LAST_RECORDED_MONDAY -> UPDATE_NEEDED')
        return True

    lastServicesHash = ConfigManager.getConfig('SERVICES_HASH')
    TRACE('LAST_SERVICES_HASH: ' + str(lastServicesHash))
    TRACE('NEW_SERVICES_HASH: ' + str(servicesHash))
    if (lastServicesHash != servicesHash):
        TRACE('SERVICES_HASH_DIFFERENCE -> UPDATE_NEEDED')
        return True

    TRACE('NO_UPDATE_NEEDED')
    return False