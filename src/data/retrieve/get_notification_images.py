from src.data.manager.notifications_manager import getNotifications
from src.share.trace import TRACE

def getNotificationImages(notificationName, notificationURL):
    NOTIFICATIONS = getNotifications()
    imagesFileNamePattern = NOTIFICATIONS[notificationName]['IMAGES_FILE_NAME_PATTERN']
    numOfPages = NOTIFICATIONS[notificationName]['NUM_OF_PAGES']
    imagesPathPattern = 'data/data/notificationsFiles/' + imagesFileNamePattern
    imagesPathList = [imagesPathPattern + str(pageNum) + '.png'
                      for pageNum in range(1, numOfPages + 1)]
    TRACE('Found notification images: ' + str(imagesPathList))

    # list may be empty due to only UTF-8 SDL support upon deploying
    return imagesPathList