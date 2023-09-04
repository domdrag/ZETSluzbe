from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem

from src.screen.main.tabs.utils.statistic_component import StatisticComponent

from src.data.share.read_statistics import readStatistics
from src.data.share.statistics_manager import getDriverStatistics
from src.data.share.get_current_month_format import getCurrentMonthFormat

class StatisticsTab(MDFloatLayout, MDTabsBase):
    statisticsTabRecycleView = ObjectProperty(None)  # left for clarity
    currentMonthFormat = StringProperty(None)
    offNum = ''

    def __init__(self, **kwargs):
        super(StatisticsTab, self).__init__(**kwargs)

    def setup(self, offNum):
        self.offNum = offNum
        self.currentMonthFormat = getCurrentMonthFormat()

        data = readStatistics(self.offNum, self.currentMonthFormat)
        if (data):
            self.statisticsTabRecycleView.data = data
            return

        errorMessage = 'Greska u sustavu. Kontaktirati administratora.'
        raise Exception(errorMessage)
    def statisticsDropDown(self):
        statistics = getDriverStatistics(self.offNum)
        monthsSortedList = list(statistics.keys())[::-1]
        monthsMenuItems = []
        for monthFormat in monthsSortedList:
            monthsMenuItems.append({'viewclass': 'OneLineListItem',
                                    'text': monthFormat,
                                    'on_release': lambda arg = monthFormat: self.changeMonth(arg)})
        self.monthsMenu = MDDropdownMenu(caller = self.ids.statisticsDropDownId,
                                         items = monthsMenuItems,
                                         position = 'bottom',
                                         ver_growth = 'down',
                                         hor_growth = 'right',
                                         width_mult = 4)
        self.monthsMenu.open()

    def changeMonth(self, monthFormat):
        # should check first if menu is opened regardless
        self.ids.statisticsDropDownId.set_item(monthFormat)
        # check if empty?
        data = readStatistics(self.offNum, monthFormat)
        self.statisticsTabRecycleView.data = data
        self.monthsMenu.dismiss()
