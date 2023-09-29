from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout

class LogsWidget(MDRelativeLayout):
    logs = StringProperty()  # binding

    def __init__(self, logs, **kwargs):
        super(LogsWidget, self).__init__(**kwargs)
        self.logs = logs
