from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout

class OffNumWidget(MDRelativeLayout):
    currentOffNum = StringProperty()  # binding

    def __init__(self, currentOffNum, **kwargs):
        super(OffNumWidget, self).__init__(**kwargs)
        self.currentOffNum = currentOffNum
