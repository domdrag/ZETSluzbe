from src.data.manager.design_manager import DesignManager
from src.data.manager.statistics_manager import StatisticsManager
from src.data.manager.config_manager import ConfigManager
from src.data.manager.update_info_manager import UpdateInfoManager
from src.data.manager.warning_messages_manager import WarningMessagesManager

def loadBasicData():
    ConfigManager.load()
    DesignManager.load()

def loadCentralData():
    StatisticsManager.load()
    UpdateInfoManager.load()
    WarningMessagesManager.load()
