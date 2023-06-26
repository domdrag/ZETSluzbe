import os

#os.environ["KIVY_NO_CONSOLELOG"] = "1" # disable all logs, needs to be ON
                                       # CERTIANLY at every release for
                                       # performance boost
import logging

logging.disable(logging.DEBUG)

from kivymd.app import MDApp
from kivy.lang import Builder

from src.screen.zet_screen_manager import ZETScreenManager
from src.data.share.color_manager import (getColors,
                                          getPrimaryColorString,
                                          getSecondaryColorString)

# novi branch 4

class ZETApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.colors = getColors()
        self.theme_cls.primary_palette = getPrimaryColorString()
        self.theme_cls.accent_palette = getSecondaryColorString()
        return Builder.load_file('design/zet_screen_manager.kv')

