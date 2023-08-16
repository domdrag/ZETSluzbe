from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty

from src.screen.main.dialogs.link import Link

class LinksWidget(RelativeLayout):
    linksWidgetRecycleView = ObjectProperty(None)  # left for clarity
    def __init__(self, linksData, *args, **kwargs):
        super(LinksWidget, self).__init__(*args, **kwargs)
        self.linksWidgetRecycleView.data = linksData