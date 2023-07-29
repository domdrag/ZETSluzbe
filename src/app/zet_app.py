from src.data.share.config_manager import loadConfig
from src.data.share.design_manager import loadDesign
from src.app.utils.environment_setup import environmentSetup

loadConfig()
loadDesign()
environmentSetup()

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import StringProperty

from src.screen.zet_screen_manager import ZETScreenManager
from src.data.share.design_manager import (getFontSize,
                                           getColors,
                                           getPrimaryColorString,
                                           getSecondaryColorString)
class ZETApp(MDApp):
    fontSize = StringProperty()

    def build(self):
        self.fontSize = getFontSize()
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.colors = getColors()
        self.theme_cls.primary_palette = getPrimaryColorString()
        self.theme_cls.accent_palette = getSecondaryColorString()
        return Builder.load_file('design/zet_screen_manager.kv')

