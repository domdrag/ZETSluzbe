from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

from src.screen.login.dialogs.utils.off_num_widget import OffNumWidget

from src.data.share.design_manager import getSecondaryColor, getWhiteColor
from src.data.share.config_manager import setConfig

class OffNumDialog(MDDialog):
    def __init__(self, currentOffNum, loginScreen):
        self.show_duration = 0
        self.loginScreen = loginScreen
        title = 'Promjena zadanog sluzbenog broja'

        app = MDApp.get_running_app()
        saveButton = [MDRaisedButton(text = 'SPREMI',
                                     theme_text_color = 'Custom',
                                     md_bg_color = getSecondaryColor(),
                                     text_color = getWhiteColor(),
                                     on_release = self.saveDefaultOffNum,
                                     font_size = app.mainScreenFontSize)]

        offNumWidget = OffNumWidget(currentOffNum)
        super(OffNumDialog, self).__init__(type = 'custom',
                                           title = title,
                                           size_hint = (0.6, None),
                                           content_cls = offNumWidget,
                                           buttons = saveButton)

    def saveDefaultOffNum(self, button):
        newDefaultOffNum = self.content_cls.offNumChangeTextFieldObj.text
        setConfig('OFFICIAL_NUMBER_STARTUP', newDefaultOffNum)
        self.loginScreen.changeCurrentOffNum(newDefaultOffNum)
        self.dismiss()
