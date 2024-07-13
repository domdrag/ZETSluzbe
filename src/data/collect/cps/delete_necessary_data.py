import os

from src.share.filenames import (CENTRAL_DATA_DIR, PRIMARY_WORK_DAY_RULES_FILE_PREFIX,
                                 PRIMARY_SATURDAY_RULES_FILE_PREFIX, PRIMARY_SUNDAY_RULES_FILE_PREFIX)
from src.share.trace import TRACE

def deleteOldSpecialDayFiles():
    # need to delete these files so we don't end up with garbage files
    dataDirsAndFiles = os.listdir(CENTRAL_DATA_DIR)
    specialDayOldFilesFound = False
    for item in dataDirsAndFiles:
        if ('[' in item and ']' in item):
            specialDayOldFilesFound = True
            filePathToRemove = CENTRAL_DATA_DIR + item
            TRACE('Removing ' + filePathToRemove)
            os.remove(CENTRAL_DATA_DIR + item)

def deleteNecessaryData():
    deleteOldSpecialDayFiles()

    oldWorkDayResourcesFound = False
    oldSaturdayResourceFound =  False
    oldSundayResourcesFound = False

    dataDirsAndFiles = os.listdir(CENTRAL_DATA_DIR)
    for item in dataDirsAndFiles:
        if (PRIMARY_WORK_DAY_RULES_FILE_PREFIX in item):
            oldWorkDayResourcesFound = True
        if PRIMARY_SATURDAY_RULES_FILE_PREFIX in item:
            oldSaturdayResourceFound = True
        if PRIMARY_SUNDAY_RULES_FILE_PREFIX in item:
            oldSundayResourcesFound = True

    return {'canUseOldWorkDayResources':  oldWorkDayResourcesFound,
            'canUseOldSaturdayResources': oldSaturdayResourceFound,
            'canUseOldSundayResources': oldSundayResourcesFound}