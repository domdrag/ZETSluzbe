from src.data.admin.utils.dropbox_admin import uploadData
from src.data.admin.utils.compress_util import compressData

def uploadDataToDropbox():
    compressData()
    uploadData()
