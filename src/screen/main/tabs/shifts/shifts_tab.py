from kivy.uix.screenmanager import Screen
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import ObjectProperty

from src.screen.main.tabs.shifts.utils.python.daily_shift import DailyShift
from src.screen.main.tabs.shifts.utils.python.call_info_popup import \
     CallInfoPopup
from src.screen.share.calendar.calendar_popup import CalendarPopup

from src.data.share.get_calendar_info import getCalendarInfo

class ShiftsTab(MDFloatLayout, MDTabsBase):
    shiftsTabRecycleView = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ShiftsTab, self).__init__(**kwargs)

    def showCallInfoPopup(self, driverInfo):
        try:
            self.callInfoPopup = CallInfoPopup(driverInfo)
            self.callInfoPopup.open()
        except Exception as e:
            print(str(e))
