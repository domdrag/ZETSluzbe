import sys

from datetime import datetime

from src.share.trace import TRACE

def redirectOutput():
    sys.stdout = open('data/logs.txt', 'a', encoding='utf-8')

def resetOutput():
    sys.stdout.close()
    sys.stdout = sys.__stdout__

def beginLogging():
    #startLogging()
    TRACE('=============')
    TRACE(datetime.now())
    TRACE('=============')

def getLogs():
    #haltLogging()
    fileR = open('data/logs.txt', 'r', encoding='utf-8')
    logs = fileR.read()
    fileR.close()
    #startLogging()
    return logs

def deleteLogs():
    #haltLogging()
    fileW = open('data/logs.txt', 'w', encoding='utf-8')
    fileW.close()
    #startLogging()