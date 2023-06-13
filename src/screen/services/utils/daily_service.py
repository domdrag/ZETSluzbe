from kivy.uix.boxlayout import BoxLayout

class DailyService(BoxLayout):
    pass


'''
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ColorProperty

class DailyService(BoxLayout):
    day = StringProperty()
    service = StringProperty()
    bgColor = ColorProperty()
    
    def __init__(self, day = '', service = '', bgColor = (0,0,0,1)):
        super(DailyService, self).__init__()
        self.day = day
        self.service = service
        self.bgColor = bgColor'''
