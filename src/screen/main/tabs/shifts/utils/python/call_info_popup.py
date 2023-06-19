from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRaisedButton
from kivy.properties import StringProperty
from kivy.core.window import Window

from jnius import autoclass
from jnius import cast

from src.screen.main.tabs.shifts.utils.python.call_info_widget import \
     CallInfoWidget

from src.data.share.color_manager import (getPrimaryColor,
                                          getSecondaryColor,
                                          getWhiteColor)

DIALOG_SIZE_HINT_X = 0.62
DIALOG_SIZE_HINT_Y = 0.53

class CallInfoPopup(MDDialog):
    name = StringProperty() # binding
    phoneNumber = StringProperty() # binding
    
    def __init__(self, driverInfo):
        if('\n' not in driverInfo):
            raise Exception('Nema telefonskog broja u bazi')
        
        driverInfoList = driverInfo.split('\n')
        self.name = driverInfoList[0]
        self.phoneNumber = driverInfoList[1]
        
        buttons=[
            MDRaisedButton(
                text = 'SPREMI U IMENIK',
                theme_text_color = 'Custom',
                md_bg_color = getSecondaryColor(),
                text_color = getWhiteColor(),
                on_release = self.saveContact
            ),
            MDRaisedButton(
                text = 'NAZOVI',
                theme_text_color = 'Custom',
                md_bg_color = getSecondaryColor(),
                text_color = getWhiteColor(),
                on_release = self.callNumber
            )]

        #widgetHeight = DIALOG_SIZE_HINT_Y * Window.size[1]
        callInfoWidget = CallInfoWidget(self.name,
                                        self.phoneNumber)
        super(CallInfoPopup, self).__init__(title = 'Kolega',
                                            type = 'custom',
                                            size_hint = (0.8, None),
                                            content_cls = callInfoWidget,
                                            buttons = buttons)
            
    def callNumber(self, button):
        Intent = autoclass('android.content.Intent')        
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Uri = autoclass('android.net.Uri')
        intent = Intent(Intent.ACTION_DIAL)         
        intent.setData(Uri.parse("tel:" + self.phoneNumber))     
        currentActivity = cast('android.app.Activity',
                               PythonActivity.mActivity)                                                   
        currentActivity.startActivity(intent)

    def saveContact(self, button):      
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Contact = autoclass('org.test.Contact') # buildozer.spec
        #Contact = autoclass('Contact')
        currentActivity = cast('android.app.Activity',
                               PythonActivity.mActivity)
        Contact.addContact(currentActivity, self.name.title(),
                           self.phoneNumber.title())
    
