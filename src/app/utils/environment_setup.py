import os
import logging
import sys

from src.data.manager.config_manager import ConfigManager
from src.share.trace import TRACE

def environmentSetup():
    if (not ConfigManager.getConfig('LOGS')):
        TRACE('NO LOGS')
        os.environ['KIVY_NO_CONSOLELOG'] = '1'
    os.environ['KIVY_ORIENTATION'] = ConfigManager.getConfig('APP_ORIENTATION')

