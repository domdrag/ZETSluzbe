from kivy.uix.widget import Widget
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField

from src.data.share.design_manager import getDesign

class LoginScreenDesign(Widget):
    def __init__(self, *args, **kwargs):
        super(LoginScreenDesign, self).__init__(*args, **kwargs)
        design = getDesign('LOGIN')

        self.fontSize = design['FONT_SIZE']
        
