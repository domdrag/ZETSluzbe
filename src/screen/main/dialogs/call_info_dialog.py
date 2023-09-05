from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRaisedButton

from jnius import autoclass
from jnius import cast

from src.screen.main.dialogs.utils.call_info_widget import CallInfoWidget

from src.data.share.design_manager import (getSecondaryColor,
                                          getWhiteColor)

class CallInfoDialog(MDDialog):
    def __init__(self, driverInfo):
        if('\n' not in driverInfo):
            raise Exception('Nema telefonskog broja u bazi')
        self.show_duration = 0
        driverInfoList = driverInfo.split('\n')
        self.name = driverInfoList[0]
        self.phoneNumber = driverInfoList[1]

        app = MDApp.get_running_app()
        buttons=[
            MDRaisedButton(
                text = 'SPREMI U IMENIK',
                theme_text_color = 'Custom',
                md_bg_color = getSecondaryColor(),
                text_color = getWhiteColor(),
                on_release = self.saveContact,
                font_size = app.mainScreenFontSize
            ),
            MDRaisedButton(
                text = 'NAZOVI',
                theme_text_color = 'Custom',
                md_bg_color = getSecondaryColor(),
                text_color = getWhiteColor(),
                font_size = app.mainScreenFontSize
            )]

        callInfoWidget = CallInfoWidget(self.name,
                                        self.phoneNumber)
        super(CallInfoDialog, self).__init__(title = 'Kolega',
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
        Contact = autoclass('org.zet_app.Contact') # buildozer.spec
        currentActivity = cast('android.app.Activity',
                               PythonActivity.mActivity)
        Contact.addContact(currentActivity, self.name.title(),
                           self.phoneNumber.title())
    
