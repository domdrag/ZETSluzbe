import requests

from src.share.trace import TRACE
from src.share.assert_throw import ASSERT_THROW

def downloadPDFFile(url, dirPath, fileName):
    filePath = dirPath + fileName

    downloadComplete = False
    while not downloadComplete:
        try:
            with requests.get(url) as r:
                ASSERT_THROW(r.status_code == 200,
                             'Greska pri skidanju file-a: ' + fileName)
                with open(filePath, 'wb') as f:
                    f.write(r.content)
            downloadComplete = True
        except Exception as e:
            TRACE(e)
        
    return filePath
