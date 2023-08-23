from src.data.share.config_manager import setConfig

def setNewConfig(mondayDateList, missingServices, servicesHash):
    setConfig('LAST_RECORD_DATE', mondayDateList)
    setConfig('MISSING_SERVICES', missingServices)
    setConfig('SERVICES_HASH', servicesHash)
