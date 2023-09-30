from kivymd.uix.dialog import MDDialog

class LoginScreenDesign:
    pass

class InfoDialog(MDDialog, LoginScreenDesign):
    dotsTimer = None
    
    def __init__(self):
        super(InfoDialog, self).__init__(type = 'custom',
                                         title = 'Status')
        self.show_duration = 0
