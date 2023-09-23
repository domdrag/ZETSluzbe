import src.data.manager.config_manager as configManager

def TRACE(traceObj):
    config = configManager.getConfig()
    
    if (config['TRACES']):
        print(traceObj)
