from src.data.share.get_config import getConfig

def TRACE(traceObj):
    config = getConfig()
    if (config['TRACES']):
        print(traceObj)
