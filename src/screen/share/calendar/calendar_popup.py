from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog

from src.screen.share.calendar.utils.calendar_widget import CalendarWidget
from src.data.share.get_calendar_info import getCalendarInfo
from src.data.share.color_manager import getSecondaryColor

DIALOG_SIZE_HINT_X = 0.8
DIALOG_SIZE_HINT_Y = 0.6
DIALOG_X_PERCENTAGE_FOR_CONTENT = 0.925 # WORKAROUND
DIALOG_Y_PERCENTAGE_FOR_CONTENT = 0.77 # WORKAROUND

class CalendarPopup(MDDialog):
    def __init__(self, calendarInfo):
        
        dialogWidth = DIALOG_SIZE_HINT_X * Window.size[0]
        dialogHeight = DIALOG_SIZE_HINT_Y * Window.size[1]
        calendarContentSize = (DIALOG_X_PERCENTAGE_FOR_CONTENT * dialogWidth,
                               DIALOG_Y_PERCENTAGE_FOR_CONTENT * dialogHeight)
        cal = CalendarWidget(calendarInfo,
                             calendarContentSize,
                             as_popup = True,
                             touch_switch = True) 
        super(CalendarPopup, self).__init__(title = 'Kalendar',
                                            type = 'custom',
                                            content_cls = cal,
                                            size_hint = (DIALOG_SIZE_HINT_X,
                                                         DIALOG_SIZE_HINT_Y))

