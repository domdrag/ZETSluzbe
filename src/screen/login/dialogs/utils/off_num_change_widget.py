from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout

class OffNumChangeWidget(MDRelativeLayout):
    currentOffNum = StringProperty()  # binding

    def __init__(self, currentOffNum, **kwargs):
        super(OffNumChangeWidget, self).__init__(**kwargs)
        self.currentOffNum = currentOffNum
