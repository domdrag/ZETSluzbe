from kivy.app import App
from kivy.lang import Builder
from kivymd.app import MDApp

from src.screen.zet_screen_manager import ZETScreenManager

class ZETApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        #self.theme_cls.accent_palette = "Red"
        return Builder.load_file('design/screen/zet_screen_manager.kv')
