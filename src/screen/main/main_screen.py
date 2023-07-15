from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from src.screen.main.main_design import MainScreenDesign
from src.screen.main.tabs.services_tab import ServicesTab
from src.screen.main.tabs.shifts_tab import ShiftsTab
from src.screen.main.tabs.hourly_rate_tab import HourlyRateTab
from src.screen.share.calendar_dialog import CalendarDialog

from src.data.share.design_manager import updateFontSize

class MainScreen(Screen):
    offNum = ''
    mainScreenTabs = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.lockSwitch = False

    def setOffNum(self, offNum):
        self.offNum = offNum

    def calendarButton(self):
        calendarDialog = CalendarDialog(self.offNum)
        calendarDialog.open()
    
    def logoutButton(self):
        self.manager.switchToLoginScreen()

    def fontSizeSlider(self, value):
        updateFontSize('MAIN', int(value))
        
        servicesTabObj = self.ids['servicesTabId']
        recycleViewObj = servicesTabObj.ids['servicesTabRecycleViewId']
        for obj in recycleViewObj.data:
            obj['font_size'] = str(int(value)) + 'dp'
        recycleViewObj.refresh_from_data()

        shiftsTabObj = self.ids['shiftsTabId']
        shiftsRecycleViewObj = shiftsTabObj.ids['shiftsTabRecycleViewId']
        for obj in shiftsRecycleViewObj.data:
            obj['font_size'] = str(int(value)) + 'dp'
        shiftsRecycleViewObj.refresh_from_data()
        
        


