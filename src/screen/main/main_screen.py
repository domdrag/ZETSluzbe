import copy

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivymd.app import MDApp

from src.screen.main.main_design import MainScreenDesign
from src.screen.main.tabs.services_tab import ServicesTab
from src.screen.main.tabs.shifts_tab import ShiftsTab
from src.screen.main.tabs.hourly_rate_tab import HourlyRateTab
from src.screen.share.calendar_dialog import CalendarDialog

from src.data.share.design_manager import updateFontSize

def updateRecycleViewFont(recycleViewData, value):
    for obj in recycleViewData:
        obj['font_size'] = str(int(value)) + 'dp'
def updateTabFont(ids, tabId, recycleViewId, value):
    tabObj = ids[tabId]
    recycleViewObj = tabObj.ids[recycleViewId]
    updateRecycleViewFont(recycleViewObj.data, value)
    recycleViewObj.refresh_from_data()

def updateStatisticsTabFont(ids, tabId, recycleViewId, value):
    tabObj = ids[tabId]
    recycleViewObj = tabObj.ids[recycleViewId]
    updateRecycleViewFont(recycleViewObj.data, value)

    for statisticComponent in recycleViewObj.data:
        newStatisticContentData = copy.deepcopy(statisticComponent['statisticContentData'])
        updateRecycleViewFont(newStatisticContentData, value)
        statisticComponent['statisticContentData'] = newStatisticContentData
    recycleViewObj.refresh_from_data()

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
        app = MDApp.get_running_app()
        app.fontSize = str(int(value)) + 'dp'
        #updateTabFont(self.ids, 'servicesTabId', 'servicesTabRecycleViewId', value)
        #updateTabFont(self.ids, 'shiftsTabId', 'shiftsTabRecycleViewId', value)
        #updateStatisticsTabFont(self.ids,
        #                        'hourlyRateTabId',
        #                        'hourlyRateTabRecycleViewId',
        #                        value)
        
        


