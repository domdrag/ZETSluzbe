from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.uix.floatlayout import MDFloatLayout

from src.screen.main.tabs.services.utils.daily_service import DailyService
from src.screen.share.calendar.calendar_popup import CalendarPopup

from src.data.share.get_calendar_info import getCalendarInfo

class ServicesTab(MDFloatLayout, MDTabsBase):
    servicesTabRecycleView = ObjectProperty(None) # left for clarity

    def __init__(self, **kwargs):
        super(ServicesTab, self).__init__(**kwargs)
    
    def logoutButton(self):
        self.manager.switchToLoginScreen()


