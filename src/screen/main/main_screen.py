from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from src.screen.main.tabs.services.services_tab import ServicesTab
from src.screen.main.tabs.shifts.shifts_tab import ShiftsTab
from src.screen.main.tabs.hourly_rate.hourly_rate_tab import HourlyRateTab

from src.screen.share.calendar.calendar_popup import CalendarPopup
from src.data.share.get_calendar_info import getCalendarInfo

import time

SWIPE_LIMIT = 50
TAB_TITLES = ['Sluzbe', 'Smjena', 'Satnica']
MAX_TABS = 3

class MainScreen(Screen):
    offNum = ''
    calendarPopup = None
    mainScreenTabs = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.currentTab = 0
        self.lockSwitch = False

    def on_enter(self):
        print('hi')

    def setOffNum(self, offNum):
        self.offNum = offNum

    def calendarButton(self):
        calendarInfo = getCalendarInfo(self.offNum)
        self.calendarPopup = CalendarPopup(calendarInfo)
        self.calendarPopup.open()

    '''
    # I don't like Kivy's default swiping distance for tabs
    def on_touch_move(self, touch):
        if (self.lockSwitch):
            return
        
        if touch.dpos[0] < -SWIPE_LIMIT:
            if self.currentTab == MAX_TABS - 1:
                return
            self.lockSwitch = True
            self.currentTab = self.currentTab + 1
            newTab = TAB_TITLES[self.currentTab]
            self.mainScreenTabs.switch_tab(newTab, search_by = 'title')
            
        elif touch.dpos[0] > SWIPE_LIMIT:
            if self.currentTab == 0:
                return
            self.lockSwitch = True
            self.currentTab = self.currentTab - 1
            newTab = TAB_TITLES[self.currentTab]
            self.mainScreenTabs.switch_tab(newTab, search_by = 'title')
            
    def on_touch_up(self, touch):
        self.lockSwitch = False'''
    
    def logoutButton(self):
        self.manager.switchToLoginScreen()
