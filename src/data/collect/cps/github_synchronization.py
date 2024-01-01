from src.data.share.synchronization_util import downloadRemoteUpdateInfo, gatherRemoteCentralData
from src.data.handler.utils.load_data import loadCentralData
from src.data.manager.update_info_manager import UpdateInfoManager

from src.share.trace import TRACE

def githubSynchronization():
    downloadRemoteUpdateInfo()
    remoteServicesHash = UpdateInfoManager.getDownloadedUpdateInfo('SERVICES_HASH')
    localServicesHash = UpdateInfoManager.getUpdateInfo('SERVICES_HASH')
    if (remoteServicesHash != localServicesHash):
        TRACE('GITHUB SYNCHRONIZATION - SERVICES HASH MISMATCH')
        TRACE('PERFORMING GITHUB SYNCHRONIZATION')
        gatherRemoteCentralData()
        loadCentralData()
        UpdateInfoManager.setDataUpdated()
        TRACE('GITHUB SYNCHRONIZATION - DATA UPDATED')
    else:
        TRACE('NOT PERFORMING GITHUB SYNCHRONIZATION')