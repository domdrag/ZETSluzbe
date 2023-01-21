from src.data.collect.utils.dropbox_util import uploadData
from src.data.collect.utils.compress_util import compressData

def uploadDataToDropbox():
    compressData()
    uploadData()
