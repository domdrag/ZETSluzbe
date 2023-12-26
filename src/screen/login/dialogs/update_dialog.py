from kivymd.uix.dialog import MDDialog
from kivy.properties import StringProperty

class UpdateDialog(MDDialog):
    message = StringProperty()

    def __init__(self,):
        super(UpdateDialog, self).__init__(type = 'custom',
                                           title = 'Status',
                                           size_hint = (0.8, None))