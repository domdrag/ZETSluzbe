from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.properties import BooleanProperty

from readServices import *
from receiveServices import *
from repair import *

import threading

class DailyShift(BoxLayout):
    pass
class DailyService(BoxLayout):
    pass


Builder.load_file('layout.kv')

def show_popup(function):
    def wrap(app, *args, **kwargs):
        popup = UpdatePopup()  # Instantiate CustomPopup (could add some kwargs if you wish)
        app.done = False  # Reset the app.done BooleanProperty
        app.bind(done=popup.dismiss)  # When app.done is set to True, then popup.dismiss is fired
        popup.open()  # Show popup
        t = threading.Thread(target=function, args=[app, popup, *args], kwargs=kwargs)  # Create thread
        t.start()  # Start thread
        return t

    return wrap




class UpdatePopup(Popup):
    
    def __init__(self, **kwargs):
        super(Popup, self).__init__(**kwargs)
        #self.ids.popupMsg.text = state


class LoginScreen(Screen):
    done = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        
    def loginBtn(self):
        serviceScreen.offNum = self.ids.offNum.text
        sm.current = 'service'

    @show_popup
    def updateBtn(self, popup):
        popup.text = 'Waiting...'
        updateResult = update(1)
        
        if(updateResult == 0):
            # ALREADY UP TO DATE
            #UpdatePopup('Already up to date!').open()
            popup.text = 'Already up to date!'
        elif(updateResult == 2):
            # ERROR
            #UpdatePopup('ERROR!').open()
            popup.text = 'Already up to date!'
            repairFiles()
            print('FILES REPAIRED')
        else:
            # UPDATED
            #UpdatePopup('Updated!').open()
            popup.text = 'Already up to date!'
            updateCopyDir()
            print('COPY FILES UPDATED')


class ServiceScreen(Screen):
    offNum = ''
    
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        
    def on_enter(self):
        self.ids.serviceScreen.data = receiveServices(self.offNum)
        
    def shiftBtn(self):
        shiftScreen.offNum = self.offNum
        sm.current = 'shift'

class ShiftScreen(Screen):
    offNum = ''
    #loaded = 0
    
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        
    def on_enter(self):
        self.ids.shiftScreen.data = receiveShifts(self.offNum)
        #self.loaded = 1

    def serviceBtn(self):
        sm.current = 'service'

    
sm = ScreenManager()
loginScreen = LoginScreen(name = 'login')
serviceScreen = ServiceScreen(name = 'service')
shiftScreen = ShiftScreen(name = 'shift')

class TestApp(App):
    def build(self):
        sm.add_widget(loginScreen)
        sm.add_widget(serviceScreen)
        sm.add_widget(shiftScreen)
        return sm


if __name__ == '__main__':
    TestApp().run()
