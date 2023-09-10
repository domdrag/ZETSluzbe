from kivymd.uix.boxlayout import MDBoxLayout

from src.screen.main.dialogs.call_info_dialog import CallInfoDialog
from src.share.trace import TRACE

class DailyShift(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super(DailyShift, self).__init__(*args, **kwargs)
                
    def callInfoButton(self, driverInfo):
        try:
            self.callInfoDialog = CallInfoDialog(driverInfo)
            self.callInfoDialog.open()
        except Exception as e:
            TRACE(e)
        
