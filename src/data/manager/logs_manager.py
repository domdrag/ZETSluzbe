import sys
import logging

from datetime import datetime

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
        sys.stdout = open('data/logs.txt', 'a', encoding='utf-8')

    @staticmethod
    def resetOutput():
        sys.stdout.close()
        sys.stdout = LogsManager.__defaultStdOut__

    @staticmethod
    def beginLogging():
        logging.disable(logging.DEBUG)
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