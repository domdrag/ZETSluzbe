import shutil
import sys
#from distutils.dir_util import copy_tree

import src.data.manager.config_manager as configManager
import src.share.trace as trace

def restoreWarnings():
    shutil.copyfile('data/backup/data/warnings.txt',
                    'data/data/warnings.txt')

def updateBackupConfig(sourceConfigPath = ''):
    if (sourceConfigPath):
        shutil.copyfile(sourceConfigPath, 'data/backup/config.json')
    else:
        shutil.copyfile('data/config.json', 'data/backup/config.json')

def removeExistingBackupData():
    # remove complete directory
    shutil.rmtree('data/backup/data')

def updateBackupDir(sourceConfigPath = ''):
    updateBackupConfig(sourceConfigPath)
    removeExistingBackupData()
    shutil.copytree('data/data', 'data/backup/data')

def repairData():
    trace.TRACE('REPAIRING DATA AND CONFIG')
    try:
        # repairing data + config
        shutil.rmtree('data/data')
        shutil.copytree('data/backup', 'data')
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