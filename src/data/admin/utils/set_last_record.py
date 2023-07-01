from src.data.share.config_manager import setConfig

def setLastRecord(mondayDate):
    lastRecordDate = [mondayDate.year,
                      mondayDate.month,
                      mondayDate.day]
    setConfig('LAST_RECORD_DATE', lastRecordDate)
