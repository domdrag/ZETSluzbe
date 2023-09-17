from kivymd.uix.boxlayout import MDBoxLayout

from src.screen.main.dialogs.utils.image_viewer import ImageViewer
from src.screen.main.dialogs.utils.gallery import Gallery

from src.data.share.get_notification_images import getNotificationImages
from src.share.trace import TRACE

class Notification(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super(Notification, self).__init__(*args, **kwargs)

    def openNotification(self, notificationText):
        imagesPathList = getNotificationImages(notificationText)

        if (len(imagesPathList) == 1):
            imageViewer = ImageViewer(imagesPathList[0])
            imageViewer.open()
        elif (len(imagesPathList) > 1):
            gallery = Gallery(imagesPathList)
            gallery.open()
        else:
            # unexpected error
            TRACE('NO_NOTIFICATIONS_FOUND')
            pass
