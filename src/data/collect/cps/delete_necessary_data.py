import os
import shutil

DATA_DIR_PATH = 'data/data/'

def UnusualOldRulesPDFsFound():
    dataDirsAndFiles = os.listdir(DATA_DIR_PATH)
    for item in dataDirsAndFiles:
        if ('[' in item and ']' in item and '.pdf' in item):
            return True

    return False


def deleteNecessaryData(workDayLinks, specialDayLinks):
    numOfWorkDayLinks = len(workDayLinks)
    numOfSpecialDayLinks = len(specialDayLinks)
    if ((not UnusualOldRulesPDFsFound()) and (numOfWorkDayLinks < 2) and (numOfSpecialDayLinks == 0)):
        return {'canUseOldWorkDayResources': True}

    files = os.listdir('data/data')
    for file in files:
        # need to delete these files so we don't end up with garbage files
        # should be equivalent to the older function
        if 'rules_W' in file:
            os.remove('data/data/' + file)
    return {'canUseOldWorkDayResources': False}