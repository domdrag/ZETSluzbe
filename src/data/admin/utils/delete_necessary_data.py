import os
import shutil

def deleteNecessaryData():
    shutil.rmtree('data/temp')

    files = os.listdir('data/data')
    for file in files:
        # need to delete these files so we don't end up with garbage files
        # should be equivalent to the older function
        if 'rules' in file:
            os.remove('data/data/' + file)
