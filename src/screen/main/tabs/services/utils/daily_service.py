from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ColorProperty, StringProperty, ObjectProperty

class DailyService(MDBoxLayout):
    day: ObjectProperty()
    service: ObjectProperty()
    bg_color: ObjectProperty()
    
    def __init__(self, **kwargs):
        super(DailyService, self).__init__(**kwargs)


