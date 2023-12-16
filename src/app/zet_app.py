from src.data.manager.logs_manager import beginLogging
from src.data.manager.config_manager import loadConfig
from src.data.manager.design_manager import loadDesign
from src.app.utils.environment_setup import environmentSetup

# order important
beginLogging()
loadConfig()
environmentSetup()
loadDesign()

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import StringProperty

from src.screen.zet_screen_manager import ZETScreenManager

from src.data.manager.config_manager import getConfig
from src.data.manager.design_manager import (getLoginScreenFontSize,
                                             getMainScreenFontSize,
                                             getLogsFontSize,
                                             getGridHeight,
                                             getColors,
                                             getPrimaryColorString,
                                             getSecondaryColorString)
class ZETApp(MDApp):
    gridHeight = StringProperty()
    loginScreenFontSize = StringProperty()
    mainScreenFontSize = StringProperty()

    def build(self):
        config = getConfig()
        self.gridHeight = getGridHeight()
        self.loginScreenFontSize = getLoginScreenFontSize()
        self.mainScreenFontSize = getMainScreenFontSize()
        self.logsFontSize = getLogsFontSize()
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.colors = getColors()
        self.theme_cls.primary_palette = getPrimaryColorString()
        self.theme_cls.accent_palette = getSecondaryColorString()
        return Builder.load_file('design/zet_screen_manager.kv')

