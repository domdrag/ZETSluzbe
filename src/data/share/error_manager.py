from src.data.share.config_manager import getConfig, setConfig

def errorOccuredInLastSession():
    config = getConfig()

    if (config['UPDATE_SUCCESSFUL']):
        return False
    return True

def unsetUpdateSuccessful():
    setConfig('UPDATE_SUCCESSFUL', 0)

def setUpdateSuccessful():
    setConfig('UPDATE_SUCCESSFUL', 1)

