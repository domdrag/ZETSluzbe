import os.path
import shutil
import sys

import src.data.manager.config_manager as configManager
import src.share.trace as trace

MAIN_DATA_DIR = 'data/data'
BACKUP_MAIN_DATA_DIR = 'data/backup/data'

def updateBackupDir():
    configManager.ConfigManager.updateBackupConfig()
    shutil.rmtree(BACKUP_MAIN_DATA_DIR) # delete data dir as well as its content
    shutil.copytree(MAIN_DATA_DIR, BACKUP_MAIN_DATA_DIR)
    trace.TRACE('BACKUP DIRECTORY UPDATED')

def recoverDataFromBackup():
    trace.TRACE('RECOVERING DATA AND CONFIG')
    try:
        # repairing data + config
        if (os.path.isdir(MAIN_DATA_DIR)):
            # delete data dir as well as its content
            shutil.rmtree(MAIN_DATA_DIR)
        shutil.copytree(BACKUP_MAIN_DATA_DIR, MAIN_DATA_DIR)
        configManager.ConfigManager.recoverConfig()
    except Exception as e:
        trace.TRACE(e)
        # if repair failed -> make sure data gets proper repair in the next run and crash the app
        # manual set needed because we don't know whether copytree copied backup config
        configManager.ConfigManager.prepareConfigForForcedSystemExit()
        sys.exit()
    trace.TRACE('DATA RECOVERED')

