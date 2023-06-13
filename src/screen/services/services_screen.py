from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout

from src.screen.services.utils.daily_service import DailyService
from src.screen.share.calendar.calendar_popup import CalendarPopup

from src.data.share.get_calendar_info import getCalendarInfo

SWIPE_LIMIT = 50

class Tab(MDFloatLayout, MDTabsBase):
    pass

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

    def calendarButton(self):
        calendarInfo = getCalendarInfo(self.offNum)
        self.calendarPopup = CalendarPopup(calendarInfo)
        self.calendarPopup.open()

    def on_touch_move(self, touch):
        if touch.dpos[0] < -SWIPE_LIMIT:
            self.manager.switchToShiftsScreen()

    def logoutButton(self):
        self.manager.switchToLoginScreen()
        
