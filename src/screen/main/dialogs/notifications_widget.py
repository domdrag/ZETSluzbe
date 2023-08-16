from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty

from src.screen.main.dialogs.notification import Notification
class NotificationsWidget(RelativeLayout):
    notificationsWidgetRecycleView = ObjectProperty(None)  # left for clarity
    def __init__(self, notificationsData, *args, **kwargs):
        super(NotificationsWidget, self).__init__(*args, **kwargs)
        self.notificationsWidgetRecycleView.data = notificationsData