from kivy.uix.popup import Popup
from kivymd.uix.dialog import MDDialog

from kivy.properties import ObjectProperty
import time

DIALOG_SIZE_HINT_X = 0.8

class ServicePopup(MDDialog):
    servicePopupDailyService = ObjectProperty(None)
    
    def __init__(self, day, service, bgColor):
        # ISSUE, cannot manage to put title, but I don't need it 
        super(ServicePopup, self).__init__(size_hint = (0.8,
                                                        0.4))
        self.servicePopupDailyService.day = day
        self.servicePopupDailyService.service = service
        self.servicePopupDailyService.bg_color = bgColor


'''
from kivy.uix.popup import Popup
from kivymd.uix.dialog import MDDialog
from kivy.properties import ObjectProperty

from src.screen.services.utils.daily_service import DailyService

DIALOG_SIZE_HINT_X = 0.8

class ServicePopup(MDDialog):
    servicePopupDailyService = ObjectProperty(None)
    
    def __init__(self, day, service, bgColor):
        dailyService = DailyService(day, service, bgColor)
        super(ServicePopup, self).__init__(type = 'custom',
                                           content_cls = dailyService,
                                           size_hint = (0.8,
                                                        0.4))
        #self.servicePopupDailyService.day = day
        #self.servicePopupDailyService.service = service
        #self.servicePopupDailyService.bg_color = bgColor
'''
