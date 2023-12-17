from src.data.manager.config_manager import loadConfig
from src.data.manager.design_manager import loadDesign
from src.data.manager.statistics_manager import StatisticsManager
from src.data.manager.warning_messages_manager import WarningMessagesManager
from src.share.trace import TRACE


def loadManagersAtStartup():
    loadConfig()
    loadDesign()
    StatisticsManager.load()

def loadManagersAfterUpdate():
    loadConfig()
    StatisticsManager.load()
    TRACE('Managers loaded after update')

def initializeManagersForUpdate():
    loadConfig() # we load config so verification receives it
    WarningMessagesManager.initializeUpdate()
    StatisticsManager.initializeUpdate()