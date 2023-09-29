import os
import logging
import sys

from src.data.manager.config_manager import getConfig
from src.data.manager.backup_manager import updateBackupConfig
from src.share.trace import TRACE
from src.data.manager.logs_manager import beginLogging

def environmentSetup():
    config = getConfig()
    beginLogging()
    
    if (not config['LOGS']):
        TRACE('NO LOGS')
        os.environ['KIVY_NO_CONSOLELOG'] = '1'
    if (not config['DEBUG_LOGS']):
        TRACE('NO DEBUG LOGS')
        logging.disable(logging.DEBUG)
    if (config['UPDATE_SUCCESSFUL']): # mind at ease when changing config
        TRACE('BACKUP CONFIG UPDATED')
        updateBackupConfig()
        
    os.environ['KIVY_ORIENTATION'] = config['APP_ORIENTATION']

