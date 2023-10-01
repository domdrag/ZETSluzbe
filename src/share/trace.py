import src.data.manager.logs_manager as logsManager

def TRACE(traceObj):
    print(traceObj)
    logsManager.redirectOutput()
    print(traceObj)
    logsManager.resetOutput()

