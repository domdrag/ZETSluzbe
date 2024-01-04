### CALLED BY verify.py SCRIPT ###

import sys
import os

sys.path.append(os.path.abspath(os.path.join('../..', 'test_utils')))
sys.path.append(os.path.abspath(os.path.join('../../../..', 'ZETSluzbe')))

from fix_data import fixData, fixCollectedData
from are_dir_trees_equal import areDirTreesEqual
from custom_print import customPrint

def verifyTestPack():
    fixData()
    
    from src.data.handler.data_handler import loadDataAtStartup
    from src.data.collect.data_collector import DataCollector
    
    try:
        print('LOADING DATA FOR VERIFICATION')
        loadDataAtStartup()
        print('STARTING TO COLLECT DATA')
        dataCollector = DataCollector()
        finished = False
        while not finished:
            updateResult = dataCollector.keepCollectingData()
            finished = updateResult['finished']
        pass
    except Exception as e:
        errorMessage = 'Error occured during data collection due to: ' + str(e)
        raise Exception(errorMessage)
    
    print('DATA COLLECTION ENDED')
    print('STARTING TEST DATA VERIFICATION')
    fixCollectedData()
    return areDirTreesEqual('ZETSluzbe-Data/data', 'wanted_data')

from io import StringIO

try:
    tracesEnabled = (sys.argv[1] == '1')
    
    normalStdout = sys.stdout
    if (not tracesEnabled):
        sys.stdout = logs = StringIO()
    verificationSuccessful = verifyTestPack()
    sys.stdout = normalStdout
    
    if (verificationSuccessful):
        customPrint('PASSED')
        # suppress memory leak from pdfium
        sys.stderr = StringIO()
    else:
        raise Exception('Data collection generated wrong data')
except Exception as e:
    sys.stdout = normalStdout
    customPrint('LOGS: ')
    print(logs.getvalue())
    customPrint('Test data verification failed due to: ' + str(e))
    customPrint('FAILED')
    
    
