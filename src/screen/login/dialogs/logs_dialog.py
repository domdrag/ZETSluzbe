from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

from src.screen.login.dialogs.utils.logs_widget import LogsWidget
from src.data.manager.design_manager import getSecondaryColor, getWhiteColor
from src.data.manager.logs_manager import deleteLogs

class LogsDialog(MDDialog):
    logsDialogWidget = None

    def __init__(self, logs):
        self.logsWidget = LogsWidget(logs)

        app = MDApp.get_running_app()
        deleteLogsButton = MDRaisedButton(text='IZBRISI LOGOVE',
                                          theme_text_color='Custom',
                                          md_bg_color = getSecondaryColor(),
                                          text_color = getWhiteColor(),
                                          on_release = self.deleteLogs,
                                          font_size = app.mainScreenFontSize)

        super(LogsDialog, self).__init__(type = 'custom',
                                         title = 'Logovi',
                                         size_hint = (0.8, None),
                                         content_cls = self.logsWidget,
                                         buttons = [deleteLogsButton])

    def deleteLogs(self, button):
        deleteLogs()
        self.logsWidget.logs = ''