from functools import partial

from kivy.uix.modalview import ModalView
from kivy.core.window import Window
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.swiper import MDSwiperItem

from src.screen.main.dialogs.utils.image_viewer import ImageViewer

HALF_SCREEN_HEIGHT = Window.size[1]  * 0.5

# inhertiance order matters!
class ClickableImage(ButtonBehavior, Image):
    pass

class Gallery(ModalView):
    #swiper = ObjectProperty(None) # left for clarity

    def __init__(self, imagesPathList):
        super(Gallery, self).__init__()

        self.height = HALF_SCREEN_HEIGHT
        for imagePath in imagesPathList:
            image = ClickableImage(source = imagePath,
                                   on_release = partial(self.displayImage,
                                                        imagePath))
            self.swiper.add_widget(MDSwiperItem(image))

    def displayImage(self, imagePath, imageDummy):
        image = ImageViewer(imagePath)
        image.open()
