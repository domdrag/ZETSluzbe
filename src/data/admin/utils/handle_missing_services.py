import ast

from src.data.share.config_manager import getConfig, setConfig
from src.share.trace import TRACE

EMPTY_MISSING_SERVICES = [0,0,0,0,0,0,0]
def addWarningForMissingServices(message):
    # OK, determineWeekSchedule occurs beforehand
    fileA = open('data/data/warnings.txt', 'a', encoding='utf-8')
    fileA.write(message)
    fileA.close()

def generateMissingServicesForDriver(services):
    isMissing = lambda service: service == '' or service == ' ' or service == None
    return [int(isMissing(service)) for service in services]

def configureMissingServices():
    with open('data/data/week_services_by_driver_encrypted.txt',
              'r',
              encoding='utf-8') as file:
        weekServicesALL = file.readlines()

    firstIteration = True
    missingServices = EMPTY_MISSING_SERVICES
    for weekServicesByDriverRaw in weekServicesALL:
        weekServicesByDriver = ast.literal_eval(weekServicesByDriverRaw)
        missingServicesByDriver = generateMissingServicesForDriver(weekServicesByDriver[1:])
        if (firstIteration):
            missingServices = missingServicesByDriver
            firstIteration = False

        elif (missingServices != missingServicesByDriver):
            TRACE('ERROR_(DIFFERENT_MISSING_SERVICES)')
            raise Exception('Greska u sluzbama (nejednak broj nedostajucih sluzbi medu vozacima)')

    return missingServices

def missingServicesChanged(missingServices, oldMissingServices):
    if (missingServices == None):
        # error in services
        return False

    if (oldMissingServices != missingServices):
        return True

    return False

def countPreviouslyAddedServices(oldMissingServices):
    return sum(int(service == 0) for service in oldMissingServices)

def handleMissingServices():
    missingServices = configureMissingServices()
    TRACE('CONFIGURED_MISSING_SERVICES:_' + str(missingServices))

    if (missingServices != EMPTY_MISSING_SERVICES):
        message = 'Sustav nije uspio ocitati neke sluzbe.'
        addWarningForMissingServices(message)

    config = getConfig()
    oldMissingServices = config['MISSING_SERVICES']
    # REMARK: numberOfPreviouslyAddedServices isn't delta if for example: we added 1 service 1st time
    # and 6 services 2nd time -> numberOfPreviouslyAddedServices == 7 (not 6!)
    numberOfPreviouslyAddedServices = countPreviouslyAddedServices(oldMissingServices)
    TRACE('NUMBER_OF_PREVIOUSY_ADDED_SERVICES: ' + str(numberOfPreviouslyAddedServices))
    # REMARK: numberOfPreviouslyAddedServices is not sufficient to determine if missingServices changed
    # because if last time was OK, but we have missing services now -> numberOfPreviouslyAddedServices == 7
    hasMissingServicesChanged = missingServicesChanged(missingServices, oldMissingServices)
    TRACE('HAS_MISSING_SERVICES_CHANGED: ' + str(hasMissingServicesChanged))

    setConfig('MISSING_SERVICES', missingServices)
    return {'hasMissingServicesChanged': hasMissingServicesChanged,
            'numberOfPreviouslyAddedServices': numberOfPreviouslyAddedServices}
