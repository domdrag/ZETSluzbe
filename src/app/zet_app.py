from src.data.manager.logs_manager import LogsManager
from src.data.data_handler import loadData, recoverData
from src.app.utils.environment_setup import environmentSetup
from src.share.trace import TRACE

# order important
LogsManager.beginLogging()
loadData()
environmentSetup()

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import StringProperty

from src.screen.zet_screen_manager import ZETScreenManager
from src.data.manager.design_manager import DesignManager

class ZETApp(MDApp):
    gridHeight = StringProperty()
    loginScreenFontSize = StringProperty()
    mainScreenFontSize = StringProperty()

    def build(self):
        self.gridHeight = DesignManager.getGridHeight()
        self.loginScreenFontSize = DesignManager.getLoginScreenFontSize()
        self.mainScreenFontSize = DesignManager.getMainScreenFontSize()
        self.logsFontSize = DesignManager.getLogsFontSize()
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.colors = DesignManager.getColors()
        self.theme_cls.primary_palette = DesignManager.getPrimaryColorString()
        self.theme_cls.accent_palette = DesignManager.getSecondaryColorString()
        return Builder.load_file('design/zet_screen_manager.kv')

