#from kivy.uix.popup import Popup
from kivymd.uix.dialog import MDDialog
#from kivy.properties import StringProperty

class UpdatePopup(MDDialog):
    #text = StringProperty() # binding
    dotsTimer = None
    
    def __init__(self):
        super(UpdatePopup, self).__init__(type = 'custom')
