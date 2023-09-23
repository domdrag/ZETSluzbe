import os

from src.share.trace import TRACE

def searchImagesPaths(imagePathPattern):
    imagesPathList = []
    imageNumber = 1

    while (os.path.isfile(imagePath := imagePathPattern +
                                       str(imageNumber) +
                                       '.png')):
        TRACE('(NOTIFICATION)_IMAGE_FOUND')
        imagesPathList.append(imagePath)
        imageNumber += 1

    return imagesPathList

def getNotificationImages(notificationName, notificationURL):
    imagePathPattern = 'data/data/notificationsFiles/' + notificationName + '_page-'
    imagesPathList = searchImagesPaths(imagePathPattern)

    # list may be empty due to only UTF-8 SDL support upon deploying
    return imagesPathList