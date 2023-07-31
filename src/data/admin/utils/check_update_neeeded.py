from datetime import date

from src.data.share.config_manager import getConfig
from src.share.trace import TRACE

def checkUpdateNeeded(mondayDate, hasMissingServicesChanged):
    config = getConfig()
    lastRecordDateConfig = config['LAST_RECORD_DATE']
    lastRecordDate = date(lastRecordDateConfig[0],
                          lastRecordDateConfig[1],
                          lastRecordDateConfig[2])

    if (mondayDate != lastRecordDate):
        TRACE('MONDAY_ONLINE_DIFFERENT_FROM_LAST_RECORDED_MONDAY -> UPDATE_NEEDED')
        return {'updateNeeded': True, 'updateCause': 'DATES_DIFFERENCE'}

    if (hasMissingServicesChanged):
        TRACE('MISSING_SERVICES_CHANGED -> UPDATE_NEEDED')
        return {'updateNeeded': True, 'updateCause': 'MISSING_SERVICES'}

    return {'updateNeeded': False, 'updateCause': None}