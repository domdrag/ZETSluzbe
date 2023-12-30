import os
import shutil
import requests

from src.data.manager.config_manager import ConfigManager
from src.share.asserts import ASSERT_THROW
from src.share.trace import TRACE

CENTRAL_DATA_DIR = 'data/central_data'
COMPRESSED_CENTRAL_DATA_FILE = 'central_data.zip'
COMPRESSED_CENTRAL_DATA_PATH = 'data/temp/' + COMPRESSED_CENTRAL_DATA_FILE
MAX_TRIES = 20

def downloadCentralData():
    githubToken = ConfigManager.getConfig('GITHUB_TOKEN')
    githubURLMain = ConfigManager.getConfig('GITHUB_URL_MAIN')
    centralDataGithubPath = COMPRESSED_CENTRAL_DATA_FILE
    URL = githubURLMain + centralDataGithubPath + '?token=' + githubToken

    headers = dict()
    headers['Authorization'] = 'token ' + githubToken

    downloadComplete = False
    attemptNumber = 1

    while not downloadComplete:
        try:
            responseGET = requests.get(URL, headers=headers)
            statusCode = responseGET.status_code
            ASSERT_THROW(statusCode == 200 or statusCode == 201,
                         'Unsuccessful central data download')

            with open(COMPRESSED_CENTRAL_DATA_PATH, 'wb') as centralData:
                centralData.write(responseGET.content)
            downloadComplete = True

        except Exception as e:
            if (attemptNumber == 1):
                TRACE(e)
            if (attemptNumber > MAX_TRIES):
                raise e
            attemptNumber += 1

def decompressCentralData():
    shutil.unpack_archive(COMPRESSED_CENTRAL_DATA_PATH, CENTRAL_DATA_DIR)

def gatherRemoteCentralData():
    if (os.path.isdir(CENTRAL_DATA_DIR)):
        shutil.rmtree(CENTRAL_DATA_DIR)

    downloadCentralData()
    decompressCentralData()

