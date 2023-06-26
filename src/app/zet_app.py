from src.app.utils.config_setup import configSetup

configSetup()

from kivymd.app import MDApp
from kivy.lang import Builder

from src.screen.zet_screen_manager import ZETScreenManager
from src.data.share.color_manager import (getColors,
                                          getPrimaryColorString,
                                          getSecondaryColorString)

class ZETApp(MDApp):    
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.colors = getColors()
        self.theme_cls.primary_palette = getPrimaryColorString()
        self.theme_cls.accent_palette = getSecondaryColorString()
        return Builder.load_file('design/zet_screen_manager.kv')

