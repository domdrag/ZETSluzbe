from kivymd.app import MDApp
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivy.uix.screenmanager import Screen
from kivy.properties import (ObjectProperty,
                             BooleanProperty,
                             StringProperty,
                             ColorProperty)

from src.data.collect.data_collector import DataCollector

from src.screen.login.dialogs.off_num_change_dialog import OffNumChangeDialog
from src.screen.login.dialogs.info_dialog import InfoDialog

from src.data.retrieve.get_warning_message_info import (
    getWarningMessageInfo
    )
from src.screen.login.dialogs.utils.update_dialog_util import dataCollectionThreadWrapper
from src.data.manager.config_manager import getConfig
from src.data.manager.design_manager import updateFontSize
from src.data.manager.logs_manager import LogsManager
from src.share.trace import TRACE

class LoginScreen(Screen):
    offNumTextFieldObj = ObjectProperty(None) # object in kv
    loginButtonObj = ObjectProperty(None) # object in kv
    updateButtonObj = ObjectProperty(None) # object in kv
    logsSheetObj = ObjectProperty(None) # object in kv
    warningMessage = StringProperty() # binding
    logs = StringProperty()
    warningMessageColor = ColorProperty() # binding
    offNum = StringProperty() # binding
    updateDone = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        
        config = getConfig()
        self.offNum = config['OFFICIAL_NUMBER_STARTUP']
        self.setWarningMessage()

    def setWarningMessage(self):
        warningMessageInfo = getWarningMessageInfo()
        self.warningMessage = warningMessageInfo['message']

    def changeDefaultOffNum(self):
        currentOffNum = self.offNumTextFieldObj.text
        offNumChangeDialog = OffNumChangeDialog(currentOffNum, self)
        offNumChangeDialog.open()

    def changeCurrentOffNum(self, newOffNum):
        self.offNumTextFieldObj.text = newOffNum

    def loginButton(self):
        offNum = self.offNumTextFieldObj.text
        try:
            self.manager.switchToMainScreen(offNum)
        except Exception as e:
            errorMessage = str(e)
            TRACE(errorMessage)
            self.infoDialog = InfoDialog(errorMessage, 'Greska')
            self.infoDialog.open()

    def updateButton(self):
        # order important
        self.statusInfoDialog = InfoDialog('', 'Status')
        #self.statusInfoDialog.open()

        #LogsManager.activateLiveLogging(self.logsSheetObj, self)
        #self.logsSheetObj.open()

        #self.logsInfoDialog.auto_dismiss = False


        #self.update()
        import multiprocessing
        self.queue = multiprocessing.Queue()

        self.logsInfoDialog = InfoDialog('', 'Logovi')
        #LogsManager.activateLiveLogging(self.logsInfoDialog, queue)
        self.logsInfoDialog.open()

        from src.data.collect.start_process import tryout2
        thread = multiprocessing.Process(target=tryout2, args = [self.queue], daemon=True)

        from kivy.clock import Clock
        Clock.schedule_interval(self.idle, 0)
        thread.start()

        #thread.join()

    def idle(self, dt):
        from queue import Empty
        try:
            while True:
                msg = self.queue.get_nowait()
                self.logsInfoDialog.infoWidget.logs += str(msg)
                pass
        except Empty:
            pass

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

    def showLogsButton(self):
        logs = LogsManager.getLogs()
        infoDialog = InfoDialog(logs, 'Logovi')
        infoDialog.open()

    def showConfigButton(self):
        config = getConfig()
        configString = str(config)
        configString = configString.replace(',', ',\n')
        infoDialog = InfoDialog(configString, 'Konfiguracija')
        infoDialog.open()

    @dataCollectionThreadWrapper
    def update(self):
        dataCollector = DataCollector()
            
        finished = False
        updateResult = dict()
        self.statusInfoDialog.text = 'Dropbox sinkronizacija'
        while not finished:
            updateResult = dataCollector.keepCollectingData()
            finished = updateResult['finished']
            self.statusInfoDialog.text = updateResult['message']

        self.statusInfoDialog.dotsTimer.cancel()
        success = updateResult['success']
        error = updateResult['error']
        errorMessage = updateResult['errorMessage']
        
        if success:
            self.setWarningMessage()
            self.statusInfoDialog.text = 'Sluzbe azurirane!'
            
        elif error:
            self.statusInfoDialog.text = 'GRESKA! Dokumenti popravljeni.\n' \
                                    + errorMessage
        else:
            self.statusInfoDialog.text = 'Sluzbe jos nisu izasle!'

        self.statusInfoDialog.auto_dismiss = True
        self.logsInfoDialog.auto_dismiss = True
        LogsManager.deactivateLiveLogging()




def tryout(queue):
    dataCollector = DataCollector(queue)
    finished = False
    while not finished:
        updateResult = dataCollector.keepCollectingData()
        finished = updateResult['finished']








            

