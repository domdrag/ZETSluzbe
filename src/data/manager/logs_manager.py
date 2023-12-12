import multiprocessing
import sys

from datetime import datetime

import src.share.trace as trace
import time

class LogsManager:
    defaultStdOut = sys.stdout
    activeLogsSheet = None
    loginScreen = None
    queue = None

    @staticmethod
    def trace(traceObj):
        print(traceObj)
        LogsManager.redirectOutput()
        print(traceObj)
        LogsManager.resetOutput()

        if (LogsManager.activeLogsSheet):
            #LogsManager.activeLogsSheet.content.text += str(traceObj) + '\n'
            #LogsManager.activeLogsSheet.loginRecycleViewObj.data = [{'text': str(traceObj)}]
            #LogsManager.loginScreen.logs += str(traceObj) + '\n'
            LogsManager.activeLogsSheet.infoWidget.logs += str(traceObj) + '\n'
            #LogsManager.activeLogsSheet.infoWidget.logs = 'ha'
            #time.sleep(1)
            pass

        if (LogsManager.queue):
            print('spremio ' + str(traceObj))
            LogsManager.queue.put(str(traceObj) + '\n')


    @staticmethod
    def activateLiveLogging(queue):
        #LogsManager.activeLogsSheet = activeLogsSheet
        LogsManager.queue = queue

        #for i in range(100):
        #    LogsManager.activeLogsSheet.infoWidget.logs += 'hfdgsdfgfdsgdfg dfgf dg fdgfdgfdgfda\n'

    def deactivateLiveLogging():
        LogsManager.activeLogsSheet = None

    @staticmethod
    def redirectOutput():
        sys.stdout = open('data/logs.txt', 'a', encoding='utf-8')

    @staticmethod
    def resetOutput():
        sys.stdout.close()
        sys.stdout = LogsManager.defaultStdOut

    @staticmethod
    def beginLogging():
        trace.TRACE('=============')
        trace.TRACE(datetime.now())
        trace.TRACE('=============')

    @staticmethod
    def getLogs():
        # haltLogging()
        fileR = open('data/logs.txt', 'r', encoding='utf-8')
        logs = fileR.read()
        fileR.close()
        # startLogging()
        return logs

    @staticmethod
    def deleteLogs():
        # haltLogging()
        fileW = open('data/logs.txt', 'w', encoding='utf-8')
        fileW.close()
        # startLogging()

