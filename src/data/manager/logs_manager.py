import sys

from datetime import datetime

import src.share.trace as trace

CURRENT_STDOUT = sys.stdout

def redirectOutput():
    sys.stdout = open('data/logs.txt', 'a', encoding='utf-8')

def resetOutput():
    global CURRENT_STDOUT
    sys.stdout.close()
    sys.stdout = CURRENT_STDOUT


def beginLogging():
    trace.TRACE('=============')
    trace.TRACE(datetime.now())
    trace.TRACE('=============')

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