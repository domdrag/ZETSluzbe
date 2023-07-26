from kivymd.uix.boxlayout import MDBoxLayout

from src.screen.main.main_design import MainScreenDesign
from src.screen.main.tabs.utils.statistic_content import StatisticContent

class StatisticComponent(MDBoxLayout, MainScreenDesign):
    def __init__(self, *args, **kwargs):
        super(StatisticComponent, self).__init__(*args, **kwargs)