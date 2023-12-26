from src.data.manager.design_manager import DesignManager
from src.data.manager.statistics_manager import StatisticsManager
from src.data.manager.config_manager import ConfigManager
from src.data.collect.data_collector import DataCollector, STARTING_OUTPUT_MESSAGE

from src.data.manager.backup_manager import recoverDataFromBackup
from src.share.trace import TRACE

def loadData():
    ConfigManager.load()
    DesignManager.load()
    StatisticsManager.load()
    TRACE('DATA LOADED')

def updateData(outputStream):
    outputStream.message = STARTING_OUTPUT_MESSAGE
    dataCollector = DataCollector()
    finished = False
    while not finished:
        updateResult = dataCollector.keepCollectingData()
        finished = updateResult['finished']
        outputStream.message = updateResult['message']

    return updateResult

def recoverData():
    recoverDataFromBackup()


