from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ColorProperty, StringProperty, ObjectProperty

from src.screen.main.main_design import MainScreenDesign

class DailyService(MDBoxLayout, MainScreenDesign):
    def __init__(self, *args, **kwargs):
        super(DailyService, self).__init__(*args, **kwargs)
 


