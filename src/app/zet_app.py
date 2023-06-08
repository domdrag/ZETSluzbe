from kivy.app import App
from kivy.lang import Builder

from src.screen.zet_screen_manager import ZETScreenManager

# novi branch 2

class ZETApp(App):
    def build(self):
        return Builder.load_file('design/screen/zet_screen_manager.kv')
