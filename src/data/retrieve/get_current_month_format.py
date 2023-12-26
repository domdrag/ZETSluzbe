from src.data.manager.config_manager import ConfigManager

def getCurrentMonthFormat():
    lastRecordDate = ConfigManager.getConfig('LAST_RECORD_DATE')
    year = lastRecordDate[0]
    month = lastRecordDate[1]
    monthFormat = str(month) + '-' + str(year)
    return monthFormat