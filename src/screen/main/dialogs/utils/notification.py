import webbrowser

from kivymd.uix.boxlayout import MDBoxLayout

class Notification(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super(Notification, self).__init__(*args, **kwargs)

    def openLink(self, notificationLink):
        webbrowser.open(notificationLink)