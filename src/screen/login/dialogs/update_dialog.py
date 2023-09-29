from kivymd.uix.dialog import MDDialog

class LoginScreenDesign:
    pass

class UpdateDialog(MDDialog, LoginScreenDesign):
    dotsTimer = None
    
    def __init__(self):
        super(UpdateDialog, self).__init__(type = 'custom',
                                           title = 'Status')
        self.show_duration = 0
