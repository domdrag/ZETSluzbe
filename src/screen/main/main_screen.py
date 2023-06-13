from kivy.uix.screenmanager import Screen
from src.screen.main.tabs.services.services_tab import ServicesTab
from src.screen.main.tabs.shifts.shifts_tab import ShiftsTab
from src.screen.main.tabs.hourly_rate.hourly_rate_tab import HourlyRateTab

from src.screen.share.calendar.calendar_popup import CalendarPopup
from src.data.share.get_calendar_info import getCalendarInfo

class MainScreen(Screen):
    offNum = ''
    calendarPopup = None
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

    def setOffNum(self, offNum):
        self.offNum = offNum

    def calendarButton(self):
        calendarInfo = getCalendarInfo(self.offNum)
        self.calendarPopup = CalendarPopup(calendarInfo)
        self.calendarPopup.open()
    
    def logoutButton(self):
        self.manager.switchToLoginScreen()
