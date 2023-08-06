from src.data.share.config_manager import setConfig

def setNewConfig(mondayDate, missingServices, servicesHash):
    lastRecordDate = [mondayDate.year,
                      mondayDate.month,
                      mondayDate.day]
    setConfig('LAST_RECORD_DATE', lastRecordDate)
    setConfig('MISSING_SERVICES', missingServices)
    setConfig('SERVICES_HASH', servicesHash)
