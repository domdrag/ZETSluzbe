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

from src.data.share.read_services import readServices
from src.data.share.read_shifts import readShifts
from src.data.share.read_statistics import readStatistics
from src.data.share.design_manager import (updateFontSize,
                                           updateGridHeight)
from src.data.share.read_notifications import readNotifications
from src.data.share.read_links import readLinks

class MainScreen(Screen):
    offNum = ''
    servicesTab = ObjectProperty() # left for clarity
    shiftsTab = ObjectProperty() # left for clarity
    statisticsTab = ObjectProperty() # left for clarity
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.lockSwitch = False

    def setup(self, offNum):
        servicesData = readServices(offNum)
        shiftsData = readShifts(offNum)
        statisticsData = readStatistics(offNum)
        if (servicesData and shiftsData and statisticsData):
            self.offNum = offNum
            self.servicesTab.servicesTabRecycleView.data = servicesData
            self.shiftsTab.shiftsTabRecycleView.data = shiftsData
            self.statisticsTab.statisticsTabRecycleView.data = statisticsData
            return

        if (servicesData == None and shiftsData == None and statisticsData):
            errorMessage = 'Sluzbeni broj ne postoji!'
        elif (servicesData == [] and shiftsData == []):
            errorMessage = 'Nema aktualnih sluzbi. Probajte azurirati sluzbe.'
        else:
            errorMessage = 'Greska u sustavu. Kontaktirati administratora.'
        raise Exception(errorMessage)


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

    def increaseGridHeight(self):
        oldValue = int(self.app.gridHeight[:-2])
        newValue = oldValue + 12
        updateGridHeight(newValue)
        self.app.gridHeight = str(oldValue + 12) + 'dp'

    def decreaseGridHeight(self):
        oldValue = int(self.app.gridHeight[:-2])
        newValue = oldValue - 12
        updateGridHeight(newValue)
        self.app.gridHeight = str(oldValue - 12) + 'dp'
        


