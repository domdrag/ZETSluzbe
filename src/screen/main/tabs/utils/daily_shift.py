from kivy.uix.boxlayout import BoxLayout

from src.screen.main.tabs.utils.call_info_dialog import CallInfoDialog
from src.share.trace import TRACE

class DailyShift(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(DailyShift, self).__init__(*args, **kwargs)
                
    def callInfoButton(self, driverInfo):
        try:
            self.callInfoDialog = CallInfoDialog(driverInfo)
            self.callInfoDialog.open()
        except Exception as e:
            TRACE(e)
        
