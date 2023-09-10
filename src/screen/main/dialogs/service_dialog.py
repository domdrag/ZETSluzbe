from kivymd.uix.dialog import MDDialog
from kivy.properties import ObjectProperty
class ServiceDialog(MDDialog):
    serviceDialogRecycleView = ObjectProperty(None)
    
    def __init__(self, day, service, bgColor):
        # self.show_duration = 0 # remove animation
        super(ServiceDialog, self).__init__(size_hint = (0.8, 0.4))
        data = [{'day': day, 'service': service, 'bg_color': bgColor}]
        self.serviceDialogRecycleView.data = data