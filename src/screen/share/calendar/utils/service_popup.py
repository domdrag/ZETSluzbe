from kivy.uix.popup import Popup

from kivy.properties import ObjectProperty

class ServicePopup(Popup):
    servicePopupDailyService = ObjectProperty(None)
    
    def __init__(self, day, service, bgColor):
        super(ServicePopup, self).__init__()
        self.servicePopupDailyService.day = day
        self.servicePopupDailyService.service = service
        self.servicePopupDailyService.bg_color = bgColor
