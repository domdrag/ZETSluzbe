from kivy.uix.boxlayout import BoxLayout

from src.screen.main.tabs.utils.call_info_dialog import CallInfoDialog

class DailyShift(BoxLayout):
    def callInfoButton(self, driverInfo):
        try:
            self.callInfoDialog = CallInfoDialog(driverInfo)
            self.callInfoDialog.open()
        except Exception as e:
            print(str(e))
        
