from kivy.properties import StringProperty
from kivy.core.clipboard import Clipboard
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.widget import MDWidget

class CallInfoWidget(MDRelativeLayout):
    driverName = StringProperty() # binding
    driverPhoneNumber = StringProperty() # binding
    
    def __init__(self, driverName, driverPhoneNumber, **kwargs):
        super(CallInfoWidget, self).__init__(**kwargs)
        self.driverName = driverName
        self.driverPhoneNumber = driverPhoneNumber

    def copyNameOnClipboard(self):
        Clipboard.copy(self.driverName)

    def copyPhoneNumberOnClipboard(self):
        Clipboard.copy(self.driverPhoneNumber)
