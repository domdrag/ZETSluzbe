import os
import shutil

from src.data.manager.config_manager import TEMP_CONFIG_COPY_FILE_PATH
from src.data.manager.config_manager import getTempConfig, setTempConfig

def compressData():
    shutil.make_archive('data/temp/data', 'zip', 'data/data')

def setUpdateSuccessfulForUpload():
    tempConfig = getTempConfig()
    tempConfig['UPDATE_SUCCESSFUL'] = 1
    setTempConfig(tempConfig)

def prepareDataForTransport():
    compressData()
    # DropboxSynchronizer should have left tempConfig at this point
    if (os.path.isfile(TEMP_CONFIG_COPY_FILE_PATH)):
        os.remove(TEMP_CONFIG_COPY_FILE_PATH)
    shutil.copyfile('data/config.json', 'data/temp/config.json')
    setUpdateSuccessfulForUpload()