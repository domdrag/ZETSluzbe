from kivymd.uix.dialog import MDDialog

from src.screen.main.dialogs.utils.calendar_widget import CalendarWidget
from src.screen.main.dialogs.service_dialog import ServiceDialog

from src.data.retrieve.get_calendar_info import getCalendarInfo

class CalendarDialog(MDDialog):
    def __init__(self, offNum):
        self.show_duration = 0 # remove animation
        calendarInfo = getCalendarInfo(offNum)
        calendarWidget = CalendarWidget(calendarInfo) 
        super(CalendarDialog, self).__init__(title = 'Kalendar',
                                             type = 'custom',
                                             size_hint = (0.9, None),
                                             content_cls = calendarWidget)

    def openServiceDialog(self, serviceFullDay, service, bgColor):
        serviceDialog = ServiceDialog(serviceFullDay, service, bgColor)
        serviceDialog.open()
