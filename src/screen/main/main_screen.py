import copy

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from src.screen.main.tabs.services_tab import ServicesTab
from src.screen.main.tabs.shifts_tab import ShiftsTab
from src.screen.main.tabs.statistics_tab import StatisticsTab
from src.screen.main.dialogs.calendar_dialog import CalendarDialog
from src.screen.main.dialogs.notifications_dialog import NotificationsDialog
from src.screen.main.dialogs.links_dialog import LinksDialog
from src.screen.main.share.main_menu import MainMenu

from src.data.share.design_manager import (updateFontSize,
                                           updateGridHeight)
from src.data.share.read_notifications import readNotifications
from src.data.share.read_links import readLinks
from src.data.share.get_current_month_format import getCurrentMonthFormat
from src.share.trace import TRACE

MAIN_SCREEN_GRID_HEIGHT_DELTA = 12
MAIN_SCREEN_FONT_SIZE_RATIO = 15

class MainScreen(Screen):
    offNum = ''
    servicesTab = ObjectProperty() # left for clarity
    shiftsTab = ObjectProperty() # left for clarity
    statisticsTab = ObjectProperty() # left for clarity
    mainMenu = ObjectProperty # left for clarity
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.lockSwitch = False

    def setup(self, offNum):
        self.offNum = offNum
        self.servicesTab.setup(offNum)
        self.shiftsTab.setup(offNum)
        self.statisticsTab.setup(offNum)

    def getOffNum(self):
        return self.offNum

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
    
    def logout(self):
        self.manager.switchToLoginScreen()

    def increaseGridHeight(self):
        gridHeightOldValue = int(self.app.gridHeight[:-2])
        gridHeightNewValue = gridHeightOldValue + MAIN_SCREEN_GRID_HEIGHT_DELTA
        self.app.gridHeight = str(gridHeightNewValue) + 'dp'
        updateGridHeight(gridHeightNewValue)

        mainScreenFontSizeNewValue = int(gridHeightNewValue // MAIN_SCREEN_FONT_SIZE_RATIO)
        self.app.mainScreenFontSize = str(mainScreenFontSizeNewValue) + 'dp'
        updateFontSize('MAIN_SCREEN_FONT_SIZE', mainScreenFontSizeNewValue)

    def decreaseGridHeight(self):
        gridHeightOldValue = int(self.app.gridHeight[:-2])
        gridHeightNewValue = gridHeightOldValue - MAIN_SCREEN_GRID_HEIGHT_DELTA
        self.app.gridHeight = str(gridHeightNewValue) + 'dp'
        updateGridHeight(gridHeightNewValue)

        mainScreenFontSizeNewValue = int(gridHeightNewValue // MAIN_SCREEN_FONT_SIZE_RATIO)
        self.app.mainScreenFontSize = str(mainScreenFontSizeNewValue) + 'dp'
        updateFontSize('MAIN_SCREEN_FONT_SIZE', mainScreenFontSizeNewValue)


