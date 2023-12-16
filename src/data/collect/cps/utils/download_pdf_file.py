import requests
import shutil

from src.data.manager.config_manager import getConfig
from src.share.trace import TRACE
from src.share.asserts import ASSERT_THROW

MAX_TRIES = 20

def downloadPDFFile(url, dirPath, fileName):
    filePath = dirPath + fileName

    downloadComplete = False
    attemptNumber = 1

    config = getConfig()
    if (config['TEST_CONFIGURATION_ACTIVATED']):
        wantedDirPath = 'wanted_' + dirPath
        try:
            shutil.copyfile(wantedDirPath + fileName, filePath)
            TRACE('TEST_CONFIGURATION_ACTIVATED - skipping download of ' +
                  fileName + '; copying file from wanted_data instead')
        except Exception as e:
            TRACE('TEST_CONFIGURATION_ACTIVATED - testing old resource file for ' +
                  fileName)
            raise e
        return filePath

    # following lines aren't currently tested
    while not downloadComplete:
        try:
            with requests.get(url) as r:
                ASSERT_THROW(r.status_code == 200,
                             'Greska pri skidanju file-a: ' + fileName)
                with open(filePath, 'wb') as f:
                    f.write(r.content)
            downloadComplete = True
        except Exception as e:
            if (attemptNumber == 1):
                TRACE(e)
            if (attemptNumber > MAX_TRIES):
                raise e
            attemptNumber += 1
        
    return filePath
