from kivy.properties import ObjectProperty
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout

from src.screen.main.tabs.utils.daily_service import DailyService

class ServicesTab(MDFloatLayout, MDTabsBase):
    servicesTabRecycleView = ObjectProperty(None) # left for clarity

    def __init__(self, **kwargs):
        super(ServicesTab, self).__init__(**kwargs)


