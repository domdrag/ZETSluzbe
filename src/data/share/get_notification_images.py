import os

from src.share.trace import TRACE

def getNotificationImages(notificationName):
    imagePathPattern = 'data/data/notificationsFiles/' + notificationName + '_page-'
    imagesPathList = []

    imageNumber = 1
    print(imagePathPattern)
    print(os.listdir('data/data/notificationsFiles'))

    while (os.path.isfile(imagePath := imagePathPattern +
                                       str(imageNumber) +
                                       '.png')):
        TRACE('(NOTIFICATION)_IMAGE_FOUND')
        imagesPathList.append(imagePath)
        imageNumber += 1

    print(imagesPathList)
    return imagesPathList