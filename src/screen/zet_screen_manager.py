import os

from kivy.uix.screenmanager import ScreenManager

from src.screen.login.login_screen import LoginScreen
from src.screen.main.main_screen import MainScreen

# workaround; portrait orientation not working for some reason [?]; 
os.environ['KIVY_ORIENTATION'] = "Portrait" 

class ZETScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(ZETScreenManager, self).__init__(**kwargs)
        #self.current = 'loginScreen'

    def loginFailure(self):
        self.loginScreen.updatePopup.text = 'Greska kod dohvacanja sluzbi.'
        self.loginScreen.updatePopup.open()
            
    def updateTabs(self, offNum, servicesData, shiftsData):
        #self.mainScreen.servicesTab.servicesTabRecycleView.data = []
        #self.mainScreen.shiftsTab.shiftsTabRecycleView.data = []
        self.mainScreen.setOffNum(offNum)
        self.mainScreen.servicesTab.servicesTabRecycleView.data = \
                                                                   servicesData
        self.mainScreen.shiftsTab.shiftsTabRecycleView.data = shiftsData

    def switchToMainScreen(self):
        if self.current == 'loginScreen':
            self.transition.direction = 'down'
        else:
            self.transition.direction = 'right'
        self.current = 'mainScreen'

    def switchToLoginScreen(self):
        self.transition.direction = 'up'
        self.current = 'loginScreen'
