from src.data.utils.gather_remote_central_data import gatherRemoteCentralData
from src.data.utils.load_data_util import loadCentralData
from src.data.manager.update_info_manager import UpdateInfoManager

def githubSynchronization():
    localRecordDate = UpdateInfoManager.getUpdateInfo('RECORD_DATE')
    gatherRemoteCentralData()
    loadCentralData()
    remoteRecordDate = UpdateInfoManager.getUpdateInfo('RECORD_DATE')
    if (localRecordDate != remoteRecordDate):
        UpdateInfoManager.setDataUpdated()