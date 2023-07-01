from src.data.share.config_manager import getConfig

def TRACE(traceObj):
    config = getConfig()
    
    if (config['TRACES']):
        print(traceObj)
