import os

from kivy.uix.screenmanager import ScreenManager

from src.screen.login.login_screen import LoginScreen
from src.screen.main.main_screen import MainScreen

# WORKAROUND; portrait orientation not working for some reason [?]; 
os.environ['KIVY_ORIENTATION'] = "Portrait" 

class ZETScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(ZETScreenManager, self).__init__(**kwargs)

    def loginFailure(self):
        self.loginScreen.updateDialog.text = 'Greska kod dohvacanja sluzbi.'
        self.loginScreen.updateDialog.open()
            
    def updateTabs(self, offNum, servicesData, shiftsData):
        self.mainScreen.setOffNum(offNum)
        self.mainScreen.servicesTab.servicesTabRecycleView.data = \
                                                                   servicesData
        self.mainScreen.shiftsTab.shiftsTabRecycleView.data = shiftsData

    def switchToMainScreen(self):
        if self.current == 'loginScreen':
            self.transition.direction = 'down'
            # WORKAROUND: button shadows briefly stay after switching screen
            #self.loginScreen.loginButtonObj.opacity = 0
            #self.loginScreen.updateButtonObj.opacity = 0
        else:
            self.transition.direction = 'right'
        self.current = 'mainScreen'

    def switchToLoginScreen(self):
        self.transition.direction = 'up'
        self.current = 'loginScreen'
        # WORKAROUND: button shadows briefly stay after switching screen
        #self.loginScreen.loginButtonObj.opacity = 1
       # self.loginScreen.updateButtonObj.opacity = 1
