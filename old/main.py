from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from func import *


class LoginWindow(Screen):
    offNum = ObjectProperty(None)

    def loginBtn(self):
        offNum = self.offNum.text
        services = servicesRun(offNum, False)
        mainWindow.services = []
        self.services = services
        mainWindow.services = services
        mainWindow.offNum = offNum
        #self.reset()
        sm.current = "main"
        #print(MainWindow.services)

    def reset(self):
        pass


class MainWindow(Screen):
    services = []
    offNum = ''
    fullServices = False

    def on_enter(self):
        print(self.offNum)
        print(self.services)
        self.fullServices = False
        self.ids.offNumLabel.text = self.offNum
        table_data = []
        for i in range(len(self.services)):    
            if(self.services[i][1] == 'O'):
                table_data.append({'text':self.services[i][0],'size_hint_y':None,
                                   'height':100,'bcolor':(.05,.30,.80,1),
                                   'halign':'center', 'valign':'top'}) #append the data
                table_data.append({'text':'\n'.join(self.services[i][1:]),'size_hint_y':None,
                                   'height':300,'bcolor':(.10,.50,.150,1),
                                   'halign':'center', 'valign':'top'}) #append the data 
                
            else:
                table_data.append({'text':self.services[i][0],'size_hint_y':None,
                                   'height':100,'bcolor':(.05,.30,.80,1),
                                   'halign':'center', 'valign':'top'}) #append the data
                table_data.append({'text':'\n'.join(self.services[i][1:]),'size_hint_y':None,
                                   'height':300,'bcolor':(.06,.25,.50,1),
                                   'halign':'center', 'valign':'top'}) #append the data 

        self.ids.table_floor_layout.cols = 1 #define value of cols to the value of self.columns
        self.ids.table_floor.data = table_data #add table_data to data value
        
    def logout(self):
        sm.current = 'login'

    def changeServices(self):
        self.fullServices = not self.fullServices
        self.services = servicesRun(self.offNum, self.fullServices)
        if(self.fullServices):
            table_data = []

            i = 0
            while(i < len(self.services)):
                if(self.services[i][1] == 'O'):
                    for j in range(3):
                        table_data.append({'text':self.services[i][0],'size_hint_y':None,
                                           'height':100,'bcolor':(.05,.30,.80,1),
                                           'halign':'center', 'valign':'top'}) #append the data
                    for j in range(3):
                        table_data.append({'text':'\n'.join(self.services[i][1:]),'size_hint_y':None,
                                           'height':300,'bcolor':(.10,.50,.150,1),
                                           'halign':'center', 'valign':'top'}) #append the data
                    i = i + 1
                    
                else:
                    for j in range(3):
                        table_data.append({'text':self.services[i][0],'size_hint_y':None,
                                           'height':100,'bcolor':(.05,.30,.80,1),
                                           'halign':'center', 'valign':'top'}) #append the data
                    for j in range(3):
                        table_data.append({'text':'\n'.join(self.services[i+j][1:]),'size_hint_y':None,
                                           'height':300,'bcolor':(.06,.25,.50,1),
                                           'halign':'center', 'valign':'top'}) #append the data
                    i = i + 3

            self.ids.table_floor_layout.cols = 3 #define value of cols to the value of self.columns
            self.ids.table_floor.data = table_data #add table_data to data value
        else:
            self.on_enter()

    def reset(self):
        pass
        


class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
#db = DataBase("users.txt")

loginWindow = LoginWindow(name="login")
mainWindow = MainWindow(name="main")
screens = [loginWindow, mainWindow]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
