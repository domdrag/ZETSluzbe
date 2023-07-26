from kivymd.uix.boxlayout import MDBoxLayout

from src.screen.main.main_design import MainScreenDesign

class StatisticContent(MDBoxLayout, MainScreenDesign):
    def __init__(self, *args, **kwargs):
        super(StatisticContent, self).__init__(*args, **kwargs)