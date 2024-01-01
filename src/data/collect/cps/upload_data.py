import os
import shutil
import requests
import base64
from requests.structures import CaseInsensitiveDict

from src.data.manager.config_manager import ConfigManager
from src.share.filenames import (CENTRAL_DATA_DIR, UPDATE_INFO_FILE, UPDATE_INFO_PATH, UPLOAD_DATA_DIR,
                                 UPLOADED_UPDATE_INFO_PATH, UPLOADED_CENTRAL_DATA_PATH,
                                 UPLOADED_CENTRAL_DATA_PATH_NO_EXT, UPLOADED_CENTRAL_DATA_FILE)
from src.share.trace import TRACE
from src.share.asserts import ASSERT_THROW

def __compressCentralData__():
    if (os.path.isfile(UPLOADED_CENTRAL_DATA_PATH)):
        os.remove(UPLOADED_CENTRAL_DATA_PATH)
    shutil.make_archive(UPLOADED_CENTRAL_DATA_PATH_NO_EXT, 'zip', CENTRAL_DATA_DIR)

def __prepareUpdateInfoFileForTransport__():
    if (os.path.isfile(UPLOADED_UPDATE_INFO_PATH)):
        os.remove(UPLOADED_UPDATE_INFO_PATH)
    shutil.copyfile(UPDATE_INFO_PATH, UPLOADED_UPDATE_INFO_PATH)

def __prepareDataForTransport__():
    __compressCentralData__()
    __prepareUpdateInfoFileForTransport__()

def __uploadFile__(filePath, file):
    headers = CaseInsensitiveDict()
    headers["Authorization"] = "token " + ConfigManager.getConfig('GITHUB_TOKEN')
    data = open(filePath, 'rb').read()
    uploadURLPattern = ConfigManager.getConfig('GITHUB_UPLOAD_URL_PATTERN')
    URL = uploadURLPattern + file

    uploadComplete = False
    while (not uploadComplete):
        try:
            responseGET = requests.get(URL, headers = headers)
            statusCodeGET = responseGET.status_code
            ASSERT_THROW(statusCodeGET == 200,
                         'Unsuccessful central data check')
            oldDataFileSHA = (responseGET.json())['sha']

            messageContent = {
                'message': 'Uploading central data',
                'content': base64.b64encode(data).decode(),
                'branch': 'main',
                'sha': oldDataFileSHA
            }
            responsePUT = requests.put(URL, headers = headers,json = messageContent)
            statusCodePUT = responsePUT.status_code
            ASSERT_THROW(statusCodePUT == 200 or statusCodePUT == 201,
                         'Unsuccessful central data upload')
            uploadComplete = True
        except Exception as e:
            TRACE(e)

def uploadData():
    __prepareDataForTransport__()
    __uploadFile__(UPLOADED_CENTRAL_DATA_PATH, UPLOADED_CENTRAL_DATA_FILE)
    __uploadFile__(UPLOADED_UPDATE_INFO_PATH, UPDATE_INFO_FILE)