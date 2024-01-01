import os

from src.share.filenames import CENTRAL_DATA_DIR, PRIMARY_WORK_DAY_RULES_FILE_PREFIX
from src.share.trace import TRACE

def OldRulesFilesForSpecialDaysFoundAndDeleted():
    dataDirsAndFiles = os.listdir(CENTRAL_DATA_DIR)
    specialDayOldFilesFound = False
    for item in dataDirsAndFiles:
        if ('[' in item and ']' in item):
            specialDayOldFilesFound = True
            filePathToRemove = CENTRAL_DATA_DIR + item
            TRACE('Removing ' + filePathToRemove)
            os.remove(CENTRAL_DATA_DIR + item)

    return specialDayOldFilesFound

# Not deleting saturday/sunday files in case we want to use old resources
# Otherwise, they should be overwritten
def deleteNecessaryData(workDayLinks, specialDayLinks):
    numOfWorkDayLinks = len(workDayLinks)
    numOfSpecialDayLinks = len(specialDayLinks)
    if ((not OldRulesFilesForSpecialDaysFoundAndDeleted()) and
        (numOfWorkDayLinks < 2) and
        (numOfSpecialDayLinks == 0)):
        return {'canUseOldWorkDayResources': True}

    dataDirsAndFiles = os.listdir(CENTRAL_DATA_DIR)
    for item in dataDirsAndFiles:
        # need to delete these files so we don't end up with garbage files
        # should be equivalent to the older function
        if PRIMARY_WORK_DAY_RULES_FILE_PREFIX in item:
            os.remove(CENTRAL_DATA_DIR + item)
    return {'canUseOldWorkDayResources': False}