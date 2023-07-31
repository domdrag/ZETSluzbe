from src.data.admin.utils.prepare_data_for_transport import prepareDataForTransport
from src.data.admin.utils.dropbox_admin import uploadData

def uploadDataToDropbox():
    prepareDataForTransport()
    uploadData()
