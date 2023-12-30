import requests
import base64
from requests.structures import CaseInsensitiveDict

from src.data.manager.config_manager import ConfigManager
from src.share.trace import TRACE
from src.share.asserts import ASSERT_THROW

URL = 'https://api.github.com/repos/domdrag/ZETSluzbe-Client-Data/contents/central_data.zip'

def uploadCentralData():
    headers = CaseInsensitiveDict()
    headers["Authorization"] = "token " + ConfigManager.getConfig('GITHUB_TOKEN')
    data = open('data/temp/central_data.zip', 'rb').read()

    uploadComplete = False
    while (not uploadComplete):
        try:
            responseGET = requests.get(URL, headers = headers)
            statusCodeGET = responseGET.status_code
            ASSERT_THROW(statusCodeGET == 200,
                         'Unsuccessful central data check')
            oldDataFileSHA = (responseGET.json())['sha']

            messageContent = {
                'message': 'Uploading client data',
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
