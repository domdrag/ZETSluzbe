import shutil

from src.data.manager.config_manager import ConfigManager

def compressData():
    shutil.make_archive('data/temp/data', 'zip', 'data/data')

def prepareDataForTransport():
    compressData()
    ConfigManager.prepareConfigToTransport()