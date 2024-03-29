from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

from src.screen.login.dialogs.utils.info_widget import InfoWidget
from src.data.manager.design_manager import DesignManager
from src.data.manager.logs_manager import LogsManager

class InfoDialog(MDDialog):
    infoWidget = None

    def __init__(self, info, title):
        buttons = []
        self.infoWidget = None
        if (title == 'Logovi' or title == 'Konfiguracija'):
            self.infoWidget = InfoWidget(info)
            if (title == 'Logovi'):
                deleteLogsButton = self.createDeleteLogsButton()
                buttons.append(deleteLogsButton)
        else:
            self.text = info

        super(InfoDialog, self).__init__(type = 'custom',
                                         title = title,
                                         size_hint = (0.8, None),
                                         content_cls = self.infoWidget,
                                         buttons = buttons)

    def createDeleteLogsButton(self):
        app = MDApp.get_running_app()
        return MDRaisedButton(text='IZBRISI LOGOVE',
                              theme_text_color='Custom',
                              md_bg_color=DesignManager.getSecondaryColor(),
                              text_color=DesignManager.getWhiteColor(),
                              on_release=self.deleteLogs,
                              font_size=app.loginScreenFontSize)

    def deleteLogs(self, button):
        LogsManager.deleteLogs()
        self.infoWidget.logs = ''