from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from src.screen.shifts.utils.python.daily_shift import DailyShift
from src.screen.shifts.utils.python.call_info_popup import CallInfoPopup
from src.screen.share.calendar.calendar_popup import CalendarPopup

from src.data.share.get_calendar_info import getCalendarInfo

SWIPE_LIMIT = 50

class ShiftsScreen(Screen):
    offNum = ''
    callInfoPopup = None
    shiftsScreenRecycleView = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ShiftsScreen, self).__init__(**kwargs)
        #self.callInfoPopup = CallInfoPopup()
    
    def setOffNum(self, offNum):
        self.offNum = offNum

    def showCallInfoPopup(self, driverInfo):
        try:
            self.callInfoPopup = CallInfoPopup(driverInfo)
            self.callInfoPopup.open()
        except Exception as e:
            print(str(e))
        
    def servicesButton(self):
        self.manager.switchToServicesScreen()

    def calendarButton(self):
        calendarInfo = getCalendarInfo(self.offNum)
        self.calendarPopup = CalendarPopup(calendarInfo)
        self.calendarPopup.open()

    def on_touch_move(self, touch):
        if touch.dpos[0] > SWIPE_LIMIT:
            self.manager.switchToServicesScreen()

    def logoutButton(self):
        self.manager.switchToLoginScreen()
