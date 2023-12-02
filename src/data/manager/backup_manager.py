import os.path
import shutil
import sys

import src.data.manager.config_manager as configManager
import src.share.trace as trace

def updateBackupConfig(sourceConfigPath = ''):
    if (sourceConfigPath):
        shutil.copyfile(sourceConfigPath, 'data/backup/config.json')
    else:
        shutil.copyfile('data/config.json', 'data/backup/config.json')

def updateBackupDir(sourceConfigPath = ''):
    updateBackupConfig(sourceConfigPath)
    shutil.rmtree('data/backup/data') # delete data dir as well as its content
    shutil.copytree('data/data', 'data/backup/data')

def repairData():
    trace.TRACE('REPAIRING DATA AND CONFIG')
    try:
        # repairing data + config
        if (os.path.isdir('data/data')):
            # delete data dir as well as its content
            shutil.rmtree('data/data')
        shutil.copytree('data/backup/data', 'data/data')
        shutil.copyfile('data/backup/config.json', 'data/config.json')
    except Exception as e:
        trace.TRACE(e)
        # if repair failed -> make sure data gets proper repair in the next run and crash the app
        # manual set needed because we don't know whether copytree copied backup config
        configManager.setConfig('UPDATE_SUCCESSFUL', 0)
        sys.exit()
    trace.TRACE('DATA AND CONFIG REPAIRED')

def repairSystem():
    repairData()
    configManager.loadConfig()