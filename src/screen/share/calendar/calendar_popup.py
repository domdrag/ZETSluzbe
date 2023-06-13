from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog

from src.screen.share.calendar.utils.calendar_widget import CalendarWidget
from src.data.share.get_calendar_info import getCalendarInfo
from src.data.share.color_manager import getSecondaryColor

DIALOG_SIZE_HINT_X = 0.8
DIALOG_SIZE_HINT_Y = 0.5

class CalendarPopup(MDDialog):
    def __init__(self, calendarInfo):
        # ISSUE, CalendarWidget size won't follow Dialog by default, but
        # when I forward the wanted height of CalendarWidget, the width
        # of the widget also changes when I change size_hint_x a.k.a
        # now the widget follow the Dialog x-coordinate
        # POSSIBLE REASON - DailyService covers entire dialog screen
        calendarDialogSize = (DIALOG_SIZE_HINT_X * Window.size[0],
                              DIALOG_SIZE_HINT_Y * Window.size[1])
        cal = CalendarWidget(calendarInfo,
                             DIALOG_SIZE_HINT_Y * Window.size[1],
                             as_popup = True,
                             touch_switch = True) 
        super(CalendarPopup, self).__init__(title = 'Kalendar',
                                            type = 'custom',
                                            content_cls = cal,
                                            size_hint = (DIALOG_SIZE_HINT_X,
                                                         None))

