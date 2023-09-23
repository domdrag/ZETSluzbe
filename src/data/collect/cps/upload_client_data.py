import requests
import base64
from requests.structures import CaseInsensitiveDict

from src.data.manager.config_manager import getConfig
from src.share.trace import TRACE

URL = 'https://api.github.com/repos/domdrag/ZETSluzbe-Client-Data/contents/data.zip'

def uploadClientData():
    config = getConfig()
    headers = CaseInsensitiveDict()
    headers["Authorization"] = "token " + config['GITHUB_TOKEN']
    data = open('data/temp/data.zip', 'rb').read()

    uploadComplete = False
    while (not uploadComplete):
        try:
            responseGET = requests.get(URL, headers = headers)
            statusCodeGET = responseGET.status_code
            assert statusCodeGET == 200, 'Unsuccessful client data check'
            oldDataFileSHA = (responseGET.json())['sha']

            messageContent = {
                'message': 'Uploading client data',
                'content': base64.b64encode(data).decode(),
                'branch': 'main',
                'sha': oldDataFileSHA
            }
            responsePUT = requests.put(URL, headers = headers,json = messageContent)
            statusCodePUT = responsePUT.status_code
            assert statusCodePUT == 200 or statusCodePUT == 201, 'Unsuccessful client data upload'
            uploadComplete = True
        except Exception as e:
            TRACE(e)
