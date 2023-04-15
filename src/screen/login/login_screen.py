from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty
from kivy.properties import ColorProperty

from src.data.admin.admin_data_collector import AdminDataCollector
from src.data.user.user_data_collector import UserDataCollector
from src.screen.login.utils.update_popup import UpdatePopup

from src.data.share.read_services import readServices
from src.data.share.read_shifts import readShifts
from src.data.share.repair_all_files import repairAllFiles
from src.data.share.update_backup_dir import updateBackupDir
from src.data.share.error_manager import errorOccuredInLastSession
from src.data.share.get_warning_message_info import (
    getWarningMessageInfo
    )
from src.screen.login.utils.update_popup_util import showPopup
from src.data.user.update_required_date_check import (
    updateRequiredDateCheck
    )
from src.data.share.dropbox_share import (
    isDropboxSynchronizationNeeded,
    dropbboxSynchronization
    )

class LoginScreen(Screen):
    ADMIN = True
    offNumTextInput = ObjectProperty(None) # object in kv
    warningMessage = StringProperty() # binding
    warningMessageColor = ColorProperty() # binding
    updateDone = BooleanProperty(False)
    updatePopup = None
    
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.updatePopup = UpdatePopup()

        # if some operation haven't stopped in last session
        if errorOccuredInLastSession():
            print('REPAIR ALL FILES - ERROR IN LAST SESSION')
            repairAllFiles()
                            
        self.setWarningMessage()
        '''
        if not self.ADMIN and updateRequiredDateCheck():
            print('USER UPDATE REQUIRED DATE CHECK')
            self.update()'''

    def setWarningMessage(self):
        warningMessageInfo = getWarningMessageInfo()
        self.warningMessage = warningMessageInfo['message']
        self.warningMessageColor = warningMessageInfo['color']

    def loginButton(self):        
        offNum = self.offNumTextInput.text
        servicesData = readServices(offNum)
        shiftsData = readShifts(offNum)
        if servicesData and shiftsData:
            self.manager.updateScreens(offNum, servicesData, shiftsData)
            self.manager.switchToServicesScreen()
        else:
            self.manager.loginFailure()

    def updateButton(self):
        self.update()

    @showPopup
    def update(self):
        if self.ADMIN:
            dataCollector = AdminDataCollector()
        else:
            dataCollector = UserDataCollector()
            
        finished = False
        updateResult = dict()
        self.updatePopup.text = 'Dropbox sinkronizacija'
        while not finished:
            updateResult = dataCollector.keepCollectingData()
            finished = updateResult['finished']
            self.updatePopup.text = updateResult['message']
   
        self.updatePopup.dotsTimer.cancel()
        success = updateResult['success']
        error = updateResult['error']
        errorMessage = updateResult['errorMessage']
        warningMessage = updateResult['warningMessage']
        warningMessageColor = updateResult['warningMessageColor']
        
        if success:
            self.warningMessage = warningMessage
            self.warningMessageColor = warningMessageColor
            self.updatePopup.text = 'Sluzbe azurirane!'
            
        elif error:
            self.updatePopup.text = 'GRESKA! Dokumenti popravljeni.\n' \
                                    + errorMessage
        else:
            if self.ADMIN:
                self.updatePopup.text = 'Sluzbe jos nisu izasle!'
            else:
                self.updatePopup.text = 'Nove sluzbe jos nisu izasle na web ' \
                                        'stranici ZET-a ili jos nisu ' \
                                        'registrirane u sustavu aplikacije.'

        self.updatePopup.auto_dismiss = True













            

