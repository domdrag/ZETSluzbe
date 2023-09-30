from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout

class InfoWidget(MDRelativeLayout):
    logs = StringProperty()  # binding

    def __init__(self, logs, **kwargs):
        super(InfoWidget, self).__init__(**kwargs)
        self.logs = logs
