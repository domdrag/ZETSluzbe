from src.data.share.config_manager import loadConfig
from src.app.utils.environment_setup import environmentSetup

loadConfig()
environmentSetup()

from kivymd.app import MDApp
from kivy.lang import Builder

from src.screen.zet_screen_manager import ZETScreenManager
from src.data.share.color_manager import (getColors,
                                          getPrimaryColorString,
                                          getSecondaryColorString)
from kivy.properties import ObjectProperty
class ZETApp(MDApp):
    fontSize = ObjectProperty('20dp')

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.colors = getColors()
        self.theme_cls.primary_palette = getPrimaryColorString()
        self.theme_cls.accent_palette = getSecondaryColorString()
        return Builder.load_file('design/zet_screen_manager.kv')

