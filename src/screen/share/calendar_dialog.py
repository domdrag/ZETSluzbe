from kivymd.uix.dialog import MDDialog

from src.screen.share.utils.calendar_widget import CalendarWidget

from src.data.share.get_calendar_info import getCalendarInfo

class CalendarDialog(MDDialog):
    def __init__(self, offNum):
        self.show_duration = 0 # remove animation
        calendarInfo = getCalendarInfo(offNum)
        calendarWidget = CalendarWidget(calendarInfo) 
        super(CalendarDialog, self).__init__(title = 'Kalendar',
                                             type = 'custom',
                                             size_hint = (0.8, None),
                                             content_cls = calendarWidget)

