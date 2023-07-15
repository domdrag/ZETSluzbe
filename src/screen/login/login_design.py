from kivy.uix.widget import Widget

from src.data.share.design_manager import getDesign

class LoginScreenDesign(Widget):
    def __init__(self, *args, **kwargs):
        super(LoginScreenDesign, self).__init__(*args, **kwargs)
        design = getDesign('LOGIN')

        self.fontSize = design['FONT_SIZE']
        self.fontValue = int(self.fontSize[:2])
        
