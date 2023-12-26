from src.data.manager.statistics_manager import StatisticsManager
from src.data.manager.warning_messages_manager import WarningMessagesManager
from src.data.manager.config_manager import ConfigManager
from src.share.trace import TRACE

def initializeDataForUpdate():
    ConfigManager.initializeUpdate()
    WarningMessagesManager.initializeUpdate()
    StatisticsManager.initializeUpdate()
    TRACE('DATA INITIALIZED FOR UPDATE')

def finishDataUpdate():
    ConfigManager.finishUpdate()
    StatisticsManager.finishUpdate()
    TRACE('DATA UPDATE FINISHED')