import sys

from datetime import datetime

from src.share.trace import TRACE

def startLogging():
    sys.stdout = open('data/logs.txt', 'a', encoding='utf-8')

def haltLogging():
    sys.stdout.close()

def beginLogging():
    startLogging()
    TRACE('=============')
    TRACE(datetime.now())
    TRACE('=============')

def getLogs():
    haltLogging()
    fileR = open('data/logs.txt', 'r', encoding='utf-8')
    logs = fileR.read()
    fileR.close()
    startLogging()
    return logs

def deleteLogs():
    haltLogging()
    fileW = open('data/logs.txt', 'w', encoding='utf-8')
    fileW.close()
    startLogging()