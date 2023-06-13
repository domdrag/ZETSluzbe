from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout

class HourlyRateTab(MDFloatLayout, MDTabsBase):
    def __init__(self, **kwargs):
        super(HourlyRateTab, self).__init__(**kwargs)
