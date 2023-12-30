import os

from src.share.trace import TRACE

DATA_DIR_PATH = 'data/central_data/'

def OldRulesFilesForSpecialDaysFoundAndDeleted():
    dataDirsAndFiles = os.listdir(DATA_DIR_PATH)
    specialDayOldFilesFound = False
    for item in dataDirsAndFiles:
        if ('[' in item and ']' in item):
            specialDayOldFilesFound = True
            filePathToRemove = 'data/central_data/' + item
            TRACE('Removing ' + filePathToRemove)
            os.remove('data/central_data/' + item)

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

    dataDirsAndFiles = os.listdir(DATA_DIR_PATH)
    for item in dataDirsAndFiles:
        # need to delete these files so we don't end up with garbage files
        # should be equivalent to the older function
        if 'rules_W' in item:
            os.remove('data/central_data/' + item)
    return {'canUseOldWorkDayResources': False}