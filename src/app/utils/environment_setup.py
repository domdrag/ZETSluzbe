import os
import logging

from src.data.share.config_manager import getConfig

def environmentSetup():
    config = getConfig()
    
    if (not config['LOGS']):
        os.environ['KIVY_NO_CONSOLELOG'] = '1'
    if (not config['DEBUG_LOGS']):
        logging.disable(logging.DEBUG)
        
    os.environ['KIVY_ORIENTATION'] = config['APP_ORIENTATION']

