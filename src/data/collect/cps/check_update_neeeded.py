from datetime import date

from src.data.manager.config_manager import getConfig
from src.share.trace import TRACE
from src.data.collect.cps.utils.add_warning_message import addWarningMessage

def unexpectedMissingServicesChange(missingServices, oldMissingServices):
    # i.e. last wednesday record wasn't missing, now it's missing
    return not all(oldMissingServices[i] >= missingServices[i] for i in range(len(missingServices)))

def missingServicesChanged(missingServices, oldMissingServices):
    if (missingServices == None):
        # error in services, not possible actually
        return False

    if (oldMissingServices == missingServices):
        return False

    if (unexpectedMissingServicesChange(missingServices, oldMissingServices)):
        message = 'Neke sluzbe fale na web-stranici ZET-a,'\
                  ' ali su prethodno zapisane u sustavu.\n'
        addWarningMessage(message)
        #raise Exception('Greska u sluzbama (fale prijasnje sluzbe)')

    return True

def checkUpdateNeeded(mondayDate, missingServices, servicesHash, synchronizationNeeded):
    config = getConfig()
    lastRecordDateConfig = config['LAST_RECORD_DATE']
    lastRecordDate = date(lastRecordDateConfig[0],
                          lastRecordDateConfig[1],
                          lastRecordDateConfig[2])

    if (mondayDate != lastRecordDate):
        TRACE('MONDAY_ZET_ONLINE_DIFFERENT_FROM_LAST_RECORDED_MONDAY -> UPDATE_NEEDED')
        return {'updateNeeded': True, 'updateCause': 'DATES_DIFFERENCE'}

    oldMissingServices = config['MISSING_SERVICES']
    hasMissingServicesChanged = missingServicesChanged(missingServices, oldMissingServices)
    if (hasMissingServicesChanged):
        TRACE('OLD_MISSING_SERVICES: ' + str(oldMissingServices))
        TRACE('MISSING_SERVICES_CHANGED -> UPDATE_NEEDED')
        return {'updateNeeded': True, 'updateCause': 'MISSING_SERVICES'}

    lastServicesHash = config['SERVICES_HASH']
    TRACE('LAST_SERVICES_HASH: ' + str(lastServicesHash))
    TRACE('NEW_SERVICES_HASH: ' + str(servicesHash))
    if (not synchronizationNeeded and lastServicesHash != servicesHash):
        TRACE('ERROR_(SERVICES_HASH_UNEXPECTED_CHANGE)')
        raise Exception('Greska u sluzbama (detektirana promjena u odnosu na stare sluzbe)')

    TRACE('NO_UPDATE_NEEDED')
    return {'updateNeeded': False, 'updateCause': None}