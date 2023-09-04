
from src.data.share.config_manager import getConfig
def getCurrentMonthFormat():
    config = getConfig()
    lastRecordDate = config['LAST_RECORD_DATE']
    year = lastRecordDate[0]
    month = lastRecordDate[1]
    monthFormat = str(month) + '-' + str(year)
    return monthFormat