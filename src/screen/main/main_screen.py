import copy

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from src.screen.main.tabs.services_tab import ServicesTab
from src.screen.main.tabs.shifts_tab import ShiftsTab
from src.screen.main.tabs.statistics_tab import StatisticsTab
from src.screen.share.calendar_dialog import CalendarDialog
from src.screen.main.dialogs.notifications_dialog import NotificationsDialog
from src.screen.main.dialogs.links_dialog import LinksDialog

from src.data.share.design_manager import (updateFontSize,
                                           GRID_HEIGHT_TO_FONT_SIZE_RATIO)
from src.data.share.read_notifications import readNotifications
from src.data.share.read_links import readLinks

class MainScreen(Screen):
    offNum = ''
    mainScreenTabs = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.lockSwitch = False

    def setOffNum(self, offNum):
        self.offNum = offNum

    def calendarButton(self):
        calendarDialog = CalendarDialog(self.offNum)
        calendarDialog.open()

    def notificationsButton(self):
        notificationsData = readNotifications()
        notificationsDialog = NotificationsDialog(notificationsData)
        notificationsDialog.open()

    def linksButton(self):
        linksData = readLinks()
        linksDialog = LinksDialog(linksData)
        linksDialog.open()
    
    def logoutButton(self):
        self.manager.switchToLoginScreen()

    def fontSizeSlider(self, value):
        updateFontSize(int(value))
        self.app.gridHeight = str(int(value * GRID_HEIGHT_TO_FONT_SIZE_RATIO)) + 'dp'

    def increaseGridHeight(self):
        oldValue = int(self.app.gridHeight[:-2])
        self.app.gridHeight = str(oldValue + 12) + 'dp'
        #oldValue = int(self.app.fontSize[:-2])
        #self.app.fontSize = str(oldValue + 1) + 'dp'

    def decreaseGridHeight(self):
        oldValue = int(self.app.gridHeight[:-2])
        self.app.gridHeight = str(oldValue - 12) + 'dp'
        #oldValue = int(self.app.fontSize[:-2])
        #self.app.fontSize = str(oldValue - 1) + 'dp'
        


