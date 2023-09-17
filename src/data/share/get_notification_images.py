import os

from src.share.trace import TRACE

def getNotificationImages(notificationName):
    imagePathPattern = 'data/data/notificationsFiles/' + notificationName + '_page-'
    imagesPathList = []

    imageNumber = 1
    while (os.path.isfile(imagePath := imagePathPattern +
                                       str(imageNumber) +
                                       '.png')):
        TRACE('(NOTIFICATION)_IMAGE_FOUND')
        imagesPathList.append(imagePath)
        imageNumber += 1

    return imagesPathList