from kivymd.uix.dialog import MDDialog

from src.screen.main.dialogs.notifications_widget import NotificationsWidget

class NotificationsDialog(MDDialog):
    def __init__(self, notificationsData):
        self.show_duration = 0 # remove animation
        notificationsWidget = NotificationsWidget(notificationsData)
        super(NotificationsDialog, self).__init__(title = 'Obavijesti',
                                                  type = 'custom',
                                                  size_hint = (0.8, None),
                                                  content_cls = notificationsWidget)




