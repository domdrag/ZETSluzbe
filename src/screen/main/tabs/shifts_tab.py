from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import ObjectProperty

from src.screen.main.tabs.utils.daily_shift import DailyShift
from src.screen.main.tabs.utils.call_info_dialog import CallInfoDialog

class ShiftsTab(MDFloatLayout, MDTabsBase):
    shiftsTabRecycleView = ObjectProperty(None) # left for clarity

    def __init__(self, **kwargs):
        super(ShiftsTab, self).__init__(**kwargs)

    def showCallInfoDialog(self, driverInfo):
        try:
            self.callInfoDialog = CallInfoDialog(driverInfo)
            self.callInfoDialog.open()
        except Exception as e:
            print(str(e))
