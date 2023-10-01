import os
import shutil

DATA_DIR_PATH = 'data/data/'

def multipleOldWorkDayPDFs():
    dataDirsAndFiles = os.listdir(DATA_DIR_PATH)
    numOfOldWorkDayPDFs = 0
    for item in dataDirsAndFiles:
        if ('rules_W' in item and '.pdf' in item):
            numOfOldWorkDayPDFs += 1
    return numOfOldWorkDayPDFs > 1

def deleteNecessaryData(workDayLinks):
    numOfWorkDayLinks = len(workDayLinks)
    if ((not multipleOldWorkDayPDFs()) and (numOfWorkDayLinks < 2)):
        return {'canUseOldWorkDayResources': True}

    files = os.listdir('data/data')
    for file in files:
        # need to delete these files so we don't end up with garbage files
        # should be equivalent to the older function
        if 'rules_W' in file:
            os.remove('data/data/' + file)
    return {'canUseOldWorkDayResources': False}