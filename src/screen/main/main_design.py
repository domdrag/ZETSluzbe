from kivy.uix.widget import Widget

from src.data.share.design_manager import getDesign

class MainScreenDesign(Widget):
    def __init__(self, *args, **kwargs):
        design = getDesign('MAIN')
        self.fontSize = design['FONT_SIZE']
        self.fontValue = int(self.fontSize[:2])
        
        super(MainScreenDesign, self).__init__(*args, **kwargs)
    
