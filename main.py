from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.properties import BooleanProperty
from kivy.core.clipboard import Clipboard

from readServices import *
from receiveServices import *
from repair import *

import threading
from threading import Timer

class DailyShift(BoxLayout):
    def copyOnClipboard(self, driverInfo):
        if('\n' not in driverInfo):
            return
        phoneNumber = driverInfo.split('\n')[1]
        if(re.match(r'^\d{3}-\d{3}-\d{1,5}$', phoneNumber)):
            Clipboard.copy(phoneNumber)

    
class DailyService(BoxLayout):
    pass


Builder.load_file('layout.kv')

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

def addDots():
    if('...' in updatePopup.text):
        updatePopup.text = updatePopup.text[:-3]
    else:
        updatePopup.text = updatePopup.text + '.'

def show_popup(function):
    def wrap(app, *args, **kwargs):
        global popupTimer
        #popup = UpdatePopup()  # Instantiate CustomPopup (could add some kwargs if you wish)
        updatePopup.auto_dismiss = False
        app.done = False  # Reset the app.done BooleanProperty
        app.bind(done=updatePopup.dismiss)  # When app.done is set to True, then popup.dismiss is fired
        updatePopup.open()  # Show popup
        t = threading.Thread(target=function, args=[app, updatePopup, *args], kwargs=kwargs)  # Create thread
        #threading.Timer(1.0, addDots).start()
        popupTimer = RepeatTimer(0.5, addDots)
        popupTimer.start()
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
        self.updateWarningMessage()

    def updateWarningMessage(self):
        fileR = open('relevant/warnings.txt', 'r', encoding='utf-8')
        lines = fileR.readlines()
        fileR.close()

        if(lines == []):
            return
        
        firstMessage = lines[0].split('$')
        self.ids.warning.text = firstMessage[1]
        if(firstMessage[0] == '0'):
            self.ids.warning.color = (0.2,0.71,0.13,1)
        else:
            self.ids.warning.color = (0.96,0.74,0,1)

        for line in lines[1:]:
            self.ids.warning.text += line
    
    def loginBtn(self):
        serviceScreen.offNum = self.ids.offNum.text
        sm.current = 'service'

    @show_popup
    def updateBtn(self, popup):
        #updateResult = update(1)
        numberOfLevels = 9 # 8+1

        for i in range(numberOfLevels):
            updateResult = update(i)
            if(updateResult == '0'):
                break
            if(updateResult == '1'):
                break
            if(updateResult == '2'):
                break
            
            updatePopup.text = updateResult
            
        popupTimer.cancel()
        if(updateResult == '0'):
            # ALREADY UP TO DATE
            updatePopup.text = 'Sluzbe jos nisu izasle!'
        elif(updateResult == '2'):
            # ERROR
            repairFiles()
            updatePopup.text = 'GRESKA! Dokumenti popravljeni.'
            print('FILES REPAIRED')
        else:
            # UPDATED
            updateCopyDir()
            self.updateWarningMessage()
            updatePopup.text = 'Azurirano!'
            print('COPY FILES UPDATED')

        updatePopup.auto_dismiss = True


class ServiceScreen(Screen):
    offNum = ''
    
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        
    def on_enter(self):
        self.ids.serviceScreen.data = receiveServices(self.offNum)
        if(not self.ids.serviceScreen.data):
            updatePopup.text = 'Azuriraj sluzbe!'
            updatePopup.open()
            sm.current = 'login'
        
    def shiftBtn(self):
        shiftScreenTemp.offNum = self.offNum
        sm.current = 'shiftTemp'

class ShiftScreenTemp(Screen):
    offNum = ''
    #loaded = 0
    
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        
    def on_enter(self):
        self.ids.shiftScreenTemp.data = receiveShifts(self.offNum)
        #self.loaded = 1

    def serviceBtn(self):
        sm.current = 'service'

'''
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
'''
    
sm = ScreenManager()
loginScreen = LoginScreen(name = 'login')
serviceScreen = ServiceScreen(name = 'service')
#shiftScreen = ShiftScreen(name = 'shift')
shiftScreenTemp = ShiftScreenTemp(name = 'shiftTemp')
updatePopup = UpdatePopup()
popupTimer = RepeatTimer(0.5, addDots)

class SluzbeApp(App):
    def build(self):
        sm.add_widget(loginScreen)
        sm.add_widget(serviceScreen)
        #sm.add_widget(shiftScreen)
        sm.add_widget(shiftScreenTemp)
        return sm


if __name__ == '__main__':
    SluzbeApp().run()
