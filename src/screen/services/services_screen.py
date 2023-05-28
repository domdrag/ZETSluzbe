from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from src.screen.services.utils.daily_service import DailyService
from src.screen.share.calendar.calendar_popup import CalendarPopup

from src.data.share.get_calendar_info import getCalendarInfo

class ServicesScreen(Screen):
    offNum = ''
    servicesScreenRecycleView = ObjectProperty(None)
    calendarPopup = None

    def __init__(self, **kwargs):
        super(ServicesScreen, self).__init__(**kwargs)
    
    def setOffNum(self, offNum):
        self.offNum = offNum

    def shiftsButton(self):
        self.manager.switchToShiftsScreen()
        
    def logoutButton(self):
        self.manager.switchToLoginScreen()

    def calendarButton(self):
        calendarInfo = getCalendarInfo(self.offNum)
        self.calendarPopup = CalendarPopup(calendarInfo)
        self.calendarPopup.open()
        
