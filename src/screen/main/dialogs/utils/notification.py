from kivymd.uix.boxlayout import MDBoxLayout

from src.screen.main.dialogs.utils.image_viewer import ImageViewer
from src.screen.main.dialogs.utils.gallery import Gallery

from src.data.share.get_notification_images import getNotificationImages
from src.share.trace import TRACE

class Notification(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super(Notification, self).__init__(*args, **kwargs)

    def openNotification(self, notificationText):
        print('open notification')
        imagesPathList = getNotificationImages(notificationText)
        print('received imagesPathList')
        if (len(imagesPathList) == 1):
            imageViewer = ImageViewer(imagesPathList[0])
            imageViewer.open()
        elif (len(imagesPathList) > 1):
            print('opening gallery')
            gallery = Gallery(imagesPathList)
            print('done gallery')
            gallery.open()
        else:
            # unexpected error
            TRACE('NO_NOTIFICATIONS_FOUND')
            pass
