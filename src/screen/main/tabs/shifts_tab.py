from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import ObjectProperty

from src.screen.main.tabs.utils.daily_shift import DailyShift

from src.data.retrieve.read_shifts import readShifts

class ShiftsTab(MDFloatLayout, MDTabsBase):
    shiftsTabRecycleView = ObjectProperty(None) # left for clarity

    def __init__(self, **kwargs):
        super(ShiftsTab, self).__init__(**kwargs)

    def setup(self, offNum):
        data = readShifts(offNum)
        if (data):
            self.shiftsTabRecycleView.data = data
            return

        errorMessage = 'Greska u sustavu. Kontaktirati administratora.'
        raise Exception(errorMessage)
