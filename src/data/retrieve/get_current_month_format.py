from src.data.manager.update_info_manager import UpdateInfoManager

def getCurrentMonthFormat():
    lastRecordDate = UpdateInfoManager.getUpdateInfo('RECORD_DATE')
    year = lastRecordDate[0]
    month = lastRecordDate[1]
    monthFormat = str(month) + '-' + str(year)
    return monthFormat