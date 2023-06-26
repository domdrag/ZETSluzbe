from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import ObjectProperty

from src.screen.main.tabs.utils.daily_shift import DailyShift

class ShiftsTab(MDFloatLayout, MDTabsBase):
    shiftsTabRecycleView = ObjectProperty(None) # left for clarity

    def __init__(self, **kwargs):
        super(ShiftsTab, self).__init__(**kwargs)
