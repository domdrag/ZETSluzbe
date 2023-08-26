import os

from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from src.screen.login.login_screen import LoginScreen
from src.screen.main.main_screen import MainScreen

# WORKAROUND; portrait orientation not working for some reason [?]; 
os.environ['KIVY_ORIENTATION'] = "Portrait"
ANDROID_BACK_BUTTON_KEY = 27

class ZETScreenManager(ScreenManager):

    def __init__(self, **kwargs):
        super(ZETScreenManager, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.androidBackClick)

    def switchToMainScreen(self, offNum):
        self.mainScreen.setup(offNum)

        if self.current == 'loginScreen':
            self.transition.direction = 'down'
        else:
            self.transition.direction = 'right'
        self.current = 'mainScreen'

    def switchToLoginScreen(self):
        self.transition.direction = 'up'
        self.current = 'loginScreen'
        
    def androidBackClick(self, window, key, *largs):
        if (key == ANDROID_BACK_BUTTON_KEY and self.current == 'mainScreen'):
            self.switchToLoginScreen()
            return True # stop the propagation