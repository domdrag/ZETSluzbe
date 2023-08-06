import ast

from src.data.share.config_manager import getConfig
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

    TRACE('CONFIGURED_MISSING_SERVICES: ' + str(missingServices))

    if (missingServices != EMPTY_MISSING_SERVICES):
        message = 'Sustav nije uspio ocitati neke sluzbe.'
        addWarningForMissingServices(message)

    return missingServices