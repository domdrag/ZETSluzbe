from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from src.screen.main.tabs.services_tab import ServicesTab
from src.screen.main.tabs.shifts_tab import ShiftsTab
from src.screen.main.tabs.hourly_rate_tab import HourlyRateTab
from src.screen.share.calendar_dialog import CalendarDialog

class MainScreen(Screen):
    offNum = ''
    mainScreenTabs = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.lockSwitch = False

    def setOffNum(self, offNum):
        self.offNum = offNum

    def calendarButton(self):
        calendarDialog = CalendarDialog(self.offNum)
        calendarDialog.open()
    
    def logoutButton(self):
        self.manager.switchToLoginScreen()
