from src.data.manager.update_info_manager import UpdateInfoManager

def getCurrentMonthFormat():
    lastRecordedMondayDateList = UpdateInfoManager.getUpdateInfo('LAST_RECORDED_MONDAY_DATE')
    year = lastRecordedMondayDateList[0]
    month = lastRecordedMondayDateList[1]
    monthFormat = str(month) + '-' + str(year)
    return monthFormat