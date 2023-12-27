import os
import shutil
import requests
import zipfile

from src.data.manager.config_manager import ConfigManager
from src.share.asserts import ASSERT_THROW

CENTRAL_DATA_DIR = 'data/data'
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
    if (os.path.isdir(CENTRAL_DATA_DIR)):
        shutil.rmtree(CENTRAL_DATA_DIR)

    with zipfile.ZipFile(COMPRESSED_CENTRAL_DATA_PATH, 'r') as centralDataZIP:
        centralDataZIP.extractall(CENTRAL_DATA_DIR)

def gatherCentralData():
    downloadCentralData()
    decompressCentralData()