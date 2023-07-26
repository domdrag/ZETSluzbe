from kivy.properties import ObjectProperty
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout

from src.screen.main.tabs.utils.statistic_component import StatisticComponent

class HourlyRateTab(MDFloatLayout, MDTabsBase):
    hourlyRateTabRecycleView = ObjectProperty(None)  # left for clarity
    def __init__(self, **kwargs):
        super(HourlyRateTab, self).__init__(**kwargs)
