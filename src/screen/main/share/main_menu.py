from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivy.properties import StringProperty

from src.screen.main.dialogs.calendar_dialog import CalendarDialog
from src.screen.main.dialogs.notifications_dialog import NotificationsDialog
from src.screen.main.dialogs.links_dialog import LinksDialog

from src.data.share.read_notifications import readNotifications
from src.data.share.read_links import readLinks

class MainMenu(MDNavigationDrawer):
    def __init__(self, *args, **kwargs):
        super(MainMenu, self).__init__(*args, **kwargs)

    def calendarButton(self):
        mainScreen = self.parent
        calendarDialog = CalendarDialog(mainScreen.getOffNum())
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
        mainScreen = self.parent
        mainScreen.logout()
        self.set_state('close')