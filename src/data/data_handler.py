import os
import shutil

from src.data.manager.design_manager import DesignManager
from src.data.manager.statistics_manager import StatisticsManager
from src.data.manager.config_manager import ConfigManager
from src.data.manager.update_info_manager import UpdateInfoManager
import src.data.collect.data_collector as dataCollector

from src.data.utils.gather_central_data import gatherCentralData
from src.data.manager.backup_manager import recoverDataFromBackup
from src.share.trace import TRACE

CENTRAL_DATA_DIR = 'data/data'

def loadData():
    ConfigManager.load()
    DesignManager.load()

    if (os.path.isdir(CENTRAL_DATA_DIR)):
        shutil.rmtree(CENTRAL_DATA_DIR)
    gatherCentralData()

    StatisticsManager.load()
    UpdateInfoManager.load()
    TRACE('DATA LOADED')

def updateData(outputStream):
    outputStream.message = dataCollector.STARTING_OUTPUT_MESSAGE
    dataCollectorObj = dataCollector.DataCollector()
    finished = False
    while not finished:
        updateResult = dataCollectorObj.keepCollectingData()
        finished = updateResult['finished']
        outputStream.message = updateResult['message']

    return updateResult

def recoverData():
    #recoverDataFromBackup()
    pass


