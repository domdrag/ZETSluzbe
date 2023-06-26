from kivy.uix.boxlayout import BoxLayout

class DailyShift(BoxLayout):
    def callInfoButton(self, driverInfo):
        parent = self.parent
        # workaround
        while not (hasattr(parent, 'showCallInfoDialog') and
                   callable(getattr(parent, 'showCallInfoDialog'))): 
            parent = parent.parent
        parent.showCallInfoDialog(driverInfo)
        
