from kivy.uix.modalview import ModalView
from kivy.core.window import Window
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.image import Image

SCREEN_WIDTH = Window.size[0]

class ImageViewer(ModalView):
    def __init__(self, imagePath):
        super(ImageViewer, self).__init__()

        self.width = SCREEN_WIDTH
        scatterLayout = ScatterLayout(do_rotation = False)
        scatterLayout.add_widget(Image(source = imagePath))
        self.add_widget(scatterLayout)