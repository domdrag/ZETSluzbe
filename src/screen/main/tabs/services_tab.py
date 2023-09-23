from kivy.properties import ObjectProperty
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout

from src.data.retrieve.read_services import readServices

class ServicesTab(MDFloatLayout, MDTabsBase):
    servicesTabRecycleView = ObjectProperty(None) # left for clarity

    def __init__(self, **kwargs):
        super(ServicesTab, self).__init__(**kwargs)

    def setup(self, offNum):
        data = readServices(offNum)
        if (data):
            self.servicesTabRecycleView.data = data
            return

        if (data == None):
            errorMessage = 'Sluzbeni broj ne postoji!'
        elif (data == []):
            errorMessage = 'Nema aktualnih sluzbi. Probajte azurirati sluzbe.'
        else:
            errorMessage = 'Greska u sustavu. Kontaktirati administratora.'
        raise Exception(errorMessage)