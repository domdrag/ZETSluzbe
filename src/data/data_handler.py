from src.data.manager.design_manager import DesignManager
from src.data.manager.statistics_manager import StatisticsManager
from src.data.manager.warning_messages_manager import WarningMessagesManager
from src.data.manager.config_manager import ConfigManager
from src.data.manager.backup_manager import recoverDataFromBackup
from src.share.trace import TRACE

def loadData():
    ConfigManager.load()
    DesignManager.load()
    StatisticsManager.load()
    TRACE('DATA LOADED')

def initializeDataForUpdate():
    ConfigManager.initializeUpdate()
    WarningMessagesManager.initializeUpdate()
    StatisticsManager.initializeUpdate()
    TRACE('DATA INITIALIZED FOR UPDATE')

def finishDataUpdate():
    ConfigManager.finishUpdate()
    StatisticsManager.finishUpdate()
    TRACE('DATA UPDATE FINISHED')

def recoverData():
    recoverDataFromBackup()
    TRACE('DATA RECOVERED')

class DataUpdater:
    __outputMessage__ = ''

    #def updateData():

