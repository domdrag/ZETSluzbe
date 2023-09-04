import os
import logging

from src.data.share.config_manager import getConfig
from src.data.share.backup_manager import updateBackupConfig
from src.share.trace import TRACE

def environmentSetup():
    config = getConfig()
    
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

