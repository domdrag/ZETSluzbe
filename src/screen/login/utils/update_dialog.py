from kivymd.uix.dialog import MDDialog

class UpdateDialog(MDDialog):
    dotsTimer = None
    
    def __init__(self):
        super(UpdateDialog, self).__init__(type = 'custom')
        self.show_duration = 0
