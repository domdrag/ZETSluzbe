from kivy.app import App
from kivy.lang import Builder
from kivymd.app import MDApp

from src.screen.zet_screen_manager import ZETScreenManager

class ZETApp(MDApp):
    def build(self):
        return Builder.load_file('design/screen/zet_screen_manager.kv')
