import os
import shutil
import requests

from src.data.manager.config_manager import ConfigManager
from src.share.filenames import (CENTRAL_DATA_DIR, DOWNLOAD_DATA_DIR, DOWNLOADED_CENTRAL_DATA_PATH,
                                 DOWNLOADED_CENTRAL_DATA_FILE, DOWNLOADED_UPDATE_INFO_PATH)
from src.share.asserts import ASSERT_THROW
from src.share.trace import TRACE

MAX_TRIES = 20

def __downloadGithubFile__(filePath, file):
    githubToken = ConfigManager.getConfig('GITHUB_TOKEN')
    githubURLMain = ConfigManager.getConfig('GITHUB_DOWNLOAD_URL_PATTERN')
    URL = githubURLMain + file + '?token=' + githubToken

    headers = dict()
    headers['Authorization'] = 'token ' + githubToken

    downloadComplete = False
    attemptNumber = 1

    while not downloadComplete:
        try:
            responseGET = requests.get(URL, headers=headers)
            statusCode = responseGET.status_code
            ASSERT_THROW(statusCode == 200 or statusCode == 201, 'Unsuccessful ' + file + ' download')
            with open(filePath, 'wb') as downloadedFile:
                downloadedFile.write(responseGET.content)
            downloadComplete = True

        except Exception as e:
            if (attemptNumber == 1):
                TRACE(e)
            if (attemptNumber > MAX_TRIES):
                raise e
            attemptNumber += 1

def __downloadRemoteCentralData__():
    if (os.path.isfile(DOWNLOADED_CENTRAL_DATA_PATH)):
        os.remove(DOWNLOADED_CENTRAL_DATA_PATH)
    __downloadGithubFile__(DOWNLOADED_CENTRAL_DATA_PATH, DOWNLOADED_CENTRAL_DATA_FILE)

def __decompressCentralData__():
    if (os.path.isdir(CENTRAL_DATA_DIR)):
        shutil.rmtree(CENTRAL_DATA_DIR)
    shutil.unpack_archive(DOWNLOADED_CENTRAL_DATA_PATH, CENTRAL_DATA_DIR)

def downloadRemoteUpdateInfo():
    if (os.path.isfile(DOWNLOADED_UPDATE_INFO_PATH)):
        os.remove(DOWNLOADED_UPDATE_INFO_PATH)
    __downloadGithubFile__(DOWNLOADED_UPDATE_INFO_PATH, UPDATE_INFO_FILE)

def gatherRemoteCentralData():
    __downloadRemoteCentralData__()
    __decompressCentralData__()