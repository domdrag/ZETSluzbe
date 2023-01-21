from src.data.collect.utils.dropbox_util import downloadData, updateNeeded
from src.data.collect.utils.compress_util import decompressData

def downloadDataFromDropbox():
    if updateNeeded():
        downloadData()
        decompressData()

