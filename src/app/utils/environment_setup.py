import os
import logging

from src.data.share.config_manager import getConfig
from src.data.share.update_backup_dir import updateBackupConfig

def environmentSetup():
    config = getConfig()
    
    if (not config['LOGS']):
        os.environ['KIVY_NO_CONSOLELOG'] = '1'
    if (not config['DEBUG_LOGS']):
        logging.disable(logging.DEBUG)
    if (config['UPDATE_SUCCESSFUL']): # mind at ease when changing config
        updateBackupConfig()
        
    os.environ['KIVY_ORIENTATION'] = config['APP_ORIENTATION']

