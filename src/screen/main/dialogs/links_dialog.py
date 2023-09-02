from kivymd.uix.dialog import MDDialog

from src.screen.main.dialogs.utils.links_widget import LinksWidget

class LinksDialog(MDDialog):
    def __init__(self, linksData):
        self.show_duration = 0 # remove animation
        linksWidget = LinksWidget(linksData)
        super(LinksDialog, self).__init__(title = 'Linkovi',
                                                  type = 'custom',
                                                  size_hint = (0.8, None),
                                                  content_cls = linksWidget)




