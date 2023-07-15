from kivy.uix.screenmanager import Screen
from kivy.properties import (ObjectProperty,
                             BooleanProperty,
                             StringProperty,
                             ColorProperty)

from src.screen.login.login_design import LoginScreenDesign
from src.data.admin.admin_data_collector import AdminDataCollector
from src.data.user.user_data_collector import UserDataCollector
from src.screen.login.utils.update_dialog import UpdateDialog

from src.data.share.read_services import readServices
from src.data.share.read_shifts import readShifts
from src.data.share.repair_all_files import repairAllFiles
from src.data.share.get_warning_message_info import (
    getWarningMessageInfo
    )
from src.screen.login.utils.update_dialog_util import showDialog
from src.data.user.update_required_date_check import (
    updateRequiredDateCheck
    )
from src.data.share.dropbox_share import (
    isDropboxSynchronizationNeeded,
    dropbboxSynchronization
    )
from src.data.share.config_manager import getConfig
from src.data.share.design_manager import updateFontSize
from src.share.trace import TRACE

class LoginScreen(Screen):
    offNumTextFieldObj = ObjectProperty(None) # object in kv
    loginButtonObj = ObjectProperty(None) # object in kv
    updateButtonObj = ObjectProperty(None) # object in kv
    warningMessage = StringProperty() # binding
    warningMessageColor = ColorProperty() # binding
    offNum = StringProperty()# binding
    updateDone = BooleanProperty(False)
    
    
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        
        config = getConfig()
        self.offNum = config['OFFICIAL_NUMBER_STARTUP']
        self.admin = config['ADMIN']
        self.setWarningMessage()
        
        '''
        if not self.ADMIN and updateRequiredDateCheck():
            TRACE('USER UPDATE REQUIRED DATE CHECK')
            self.update()'''

    def setWarningMessage(self):
        warningMessageInfo = getWarningMessageInfo()
        self.warningMessage = warningMessageInfo['message']
        self.warningMessageColor = warningMessageInfo['color']

    def loginButton(self):        
        offNum = self.offNumTextFieldObj.text
        servicesData = readServices(offNum)
        shiftsData = readShifts(offNum)
        if servicesData and shiftsData:
            self.manager.updateTabs(offNum, servicesData, shiftsData)
            self.manager.switchToMainScreen()
            return

        if (servicesData == None and shiftsData == None):
            message = 'Sluzbeni broj ne postoji!'
        elif (servicesData == [] and shiftsData == []):
            message = 'Nema aktualnih sluzbi. Probajte azurirati sluzbe.'
        else:
            message = 'Greska u sustavu. Kontaktirati administratora.'

        self.updateDialog = UpdateDialog()
        self.updateDialog.text = message
        self.updateDialog.open()

    def updateButton(self):
        self.updateDialog = UpdateDialog()
        self.update()

    def fontSizeSlider(self, value):
        updateFontSize('LOGIN', int(value))
        for obj in self.ids.values():
            obj.font_size = str(int(value)) + 'dp'

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













            

