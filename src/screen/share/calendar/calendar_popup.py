from kivy.uix.popup import Popup

from src.screen.share.calendar.utils.calendar_widget import CalendarWidget
from src.data.share.get_calendar_info import getCalendarInfo

class CalendarPopup(Popup):
    def __init__(self, calendarInfo):
        cal = CalendarWidget(calendarInfo, as_popup = True) 
        super(CalendarPopup, self).__init__(title = 'Kalendar',
                                            content = cal,
                                            size_hint = (.9, .5))
 
 
