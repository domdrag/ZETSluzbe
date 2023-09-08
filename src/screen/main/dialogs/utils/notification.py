import webbrowser
#import fitz
import requests

from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.scatterlayout import ScatterLayout, Scatter
from kivy.uix.image import AsyncImage
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivymd.uix.swiper import MDSwiper, MDSwiperItem
from kivymd.uix.fitimage import FitImage
from kivy.core.window import Window
from kivy.uix.widget import Widget
import pdfplumber
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import Screen
from kivy.uix.modalview import ModalView
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

from src.share.trace import TRACE


def downloadPDFFile(url, fileName):
    filePath = 'data/temp/' + fileName

    downloadComplete = False
    while not downloadComplete:
        try:
            with requests.get(url) as r:
                assert r.status_code == 200, \
                    f'error, status code is {r.status_code}'
                with open(filePath, 'wb') as f:
                    f.write(r.content)
            downloadComplete = True
        except Exception as e:
            TRACE(e)

    return filePath

class MainCanvasAfter(Widget):
    pass
class MoinLay(RelativeLayout, MainCanvasAfter):
    pass
class MoinSwip(MDSwiper, MainCanvasAfter):
    pass
class MoinScatt(ScatterLayout, MainCanvasAfter):
    pass
class MoinScat(Scatter, MainCanvasAfter):
    pass
class MyImage(ButtonBehavior, Image):
    pass

class Notification(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super(Notification, self).__init__(*args, **kwargs)

    def openLink(self, notificationLink):
        #webbrowser.open(notificationLink)
        #import shutil
        #import os
        #shutil.rmtree('data/temp')
        #os.mkdir('data/temp')
        '''
        notificationPDF = downloadPDFFile(notificationLink, 'notification.pdf')
        dpi = 300  # choose desired dpi here
        zoom = dpi / 72  # zoom factor, standard: 72 dpi
        magnify = fitz.Matrix(zoom, zoom)  # magnifies in x, resp. y direction
        doc = fitz.open(notificationPDF)  # open document
        picList = []
        for page in doc:
            pix = page.get_pixmap(matrix=magnify)  # render page to an image
            path = f'data/temp/page-{page.number}.jpg'
            pix.save(path)
            picList.append(path)
            #pix.save('data/temp/notification.jpg')
        '''

        notificationPDF = downloadPDFFile(notificationLink, 'notification.pdf')
        picList = []
        pdf = pdfplumber.open(notificationPDF)
        for page in pdf.pages:
            path = f'data/temp/page-{page.page_number}.png'
            im = page.to_image(resolution=300)
            im.save(path)
            picList.append(path)

        #image = AsyncImage(source = 'data/temp/notification.jpg')
        #scatter.add_widget(image)
        #relativeLayout = RelativeLayout(size_hint_y = None,
        #                                height = Window.size[1])
        #relativeLayout.add_widget(scatter)
        #self.add_widget(scatter)
        size = Window.size
        mdSwiper = MDSwiper()
        mv = ModalView(size_hint_y = None,
                       height = size[1] * 0.5,
                       background = '',
                       background_color = [0,0,0,0])
        for picPath in picList:
            print(picPath)
            #scatter1 = ScatterLayout(do_translation=False,
            #                         do_rotation=False)
            from functools import partial
            im = MyImage(source = picPath,
                        allow_stretch= True,
                        keep_ratio= True,
                        on_release = partial(self.showPic,picPath))
            mdSwiper.add_widget(MDSwiperItem(im))

        mv.add_widget(mdSwiper)
        mv.open()

    def showPic(self, picPath, imageDummy):
        print('hi')
        size = Window.size
        mv = ModalView(size_hint_x=None,
                       width=size[0],
                       background='',
                       background_color=[0, 0, 0, 1])
        print(picPath)
        scatter1 = ScatterLayout(do_rotation=False)
        scatter1.add_widget(Image(source=picPath))
        mv.add_widget(scatter1)
        print('hi4')
        mv.open()