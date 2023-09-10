from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.properties import (ObjectProperty,
                             BooleanProperty,
                             StringProperty,
                             ColorProperty)

from src.data.admin.admin_data_collector import AdminDataCollector
from src.data.user.user_data_collector import UserDataCollector
from src.screen.login.dialogs.update_dialog import UpdateDialog
from src.screen.login.dialogs.off_num_dialog import OffNumDialog


from src.data.share.get_warning_message_info import (
    getWarningMessageInfo
    )
from src.screen.login.dialogs.utils.update_dialog_util import showDialog
from src.data.share.config_manager import getConfig, setConfig
from src.data.share.design_manager import updateFontSize
from src.share.trace import TRACE

class LoginScreen(Screen):
    offNumTextFieldObj = ObjectProperty(None) # object in kv
    loginButtonObj = ObjectProperty(None) # object in kv
    updateButtonObj = ObjectProperty(None) # object in kv
    warningMessage = StringProperty() # binding
    warningMessageColor = ColorProperty() # binding
    offNum = StringProperty() # binding
    updateDone = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        
        config = getConfig()
        self.offNum = config['OFFICIAL_NUMBER_STARTUP']
        self.admin = config['ADMIN']
        self.setWarningMessage()

    def toggleAdmin(self):
        self.admin = not self.admin
        self.app.isAdmin = self.admin

        setConfig('ADMIN', int(self.admin))

    def setWarningMessage(self):
        warningMessageInfo = getWarningMessageInfo()
        self.warningMessage = warningMessageInfo['message']
        self.warningMessageColor = warningMessageInfo['color']

    def changeDefaultOffNum(self):
        currentOffNum = self.offNumTextFieldObj.text
        offNumDialog = OffNumDialog(currentOffNum, self)
        offNumDialog.open()

    def changeCurrentOffNum(self, newOffNum):
        self.offNumTextFieldObj.text = newOffNum

    def loginButton(self):
        offNum = self.offNumTextFieldObj.text
        try:
            self.manager.switchToMainScreen(offNum)
        except Exception as e:
            errorMessage = str(e)
            TRACE(errorMessage)
            self.updateDialog = UpdateDialog()
            self.updateDialog.text = errorMessage
            self.updateDialog.open()

    def updateButton(self):
        self.updateDialog = UpdateDialog()
        self.update()

    def increaseFontSize(self):
        oldValue = int(self.app.loginScreenFontSize[:-2])
        newValue = oldValue + 1
        updateFontSize('LOGIN_SCREEN_FONT_SIZE', newValue)
        self.app.loginScreenFontSize = str(newValue) + 'dp'

    def decreaseFontSize(self):
        oldValue = int(self.app.loginScreenFontSize[:-2])
        newValue = oldValue - 1
        updateFontSize('LOGIN_SCREEN_FONT_SIZE', newValue)
        self.app.loginScreenFontSize = str(newValue) + 'dp'

    @showDialog
    def update(self):
        if self.admin:
            dataCollector = AdminDataCollector()
        else:
            dataCollector = UserDataCollector()
            
        finished = False
        updateResult = dict()
        self.updateDialog.text = 'Dropbox sinkronizacija'
        while not finished:
            updateResult = dataCollector.keepCollectingData()
            finished = updateResult['finished']
            self.updateDialog.text = updateResult['message']
   
        self.updateDialog.dotsTimer.cancel()
        success = updateResult['success']
        error = updateResult['error']
        errorMessage = updateResult['errorMessage']
        
        if success:
            self.setWarningMessage()
            self.updateDialog.text = 'Sluzbe azurirane!'
            
        elif error:
            self.updateDialog.text = 'GRESKA! Dokumenti popravljeni.\n' \
                                    + errorMessage
        else:
            if self.admin:
                self.updateDialog.text = 'Sluzbe jos nisu izasle!'
            else:
                self.updateDialog.text = 'Nove sluzbe jos nisu izasle na web ' \
                                        'stranici ZET-a ili jos nisu ' \
                                        'registrirane u sustavu aplikacije.'

        self.updateDialog.auto_dismiss = True













            

