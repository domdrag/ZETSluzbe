import sys
import logging

from datetime import datetime

from src.share.filenames import LOGS_PATH
import src.share.trace as trace

class LogsManager:
    __defaultStdOut__ = sys.stdout

    @staticmethod
    def trace(traceObj):
        print(traceObj)
        LogsManager.redirectOutput()
        print(traceObj)
        LogsManager.resetOutput()

    @staticmethod
    def redirectOutput():
        sys.stdout = open(LOGS_PATH, 'a', encoding='utf-8')

    @staticmethod
    def resetOutput():
        sys.stdout.close()
        sys.stdout = LogsManager.__defaultStdOut__

    @staticmethod
    def beginLogging():
        trace.TRACE('=============')
        trace.TRACE(datetime.now())
        trace.TRACE('=============')

    @staticmethod
    def getLogs():
        fileR = open(LOGS_PATH, 'r', encoding='utf-8')
        logs = fileR.read()
        fileR.close()
        return logs

    @staticmethod
    def deleteLogs():
        fileW = open(LOGS_PATH, 'w', encoding='utf-8')
        fileW.close()
