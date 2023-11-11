import os
import shutil
import pdfplumber

from src.data.manager.notifications_manager import setNotifications
from src.data.collect.cps.utils.download_pdf_file import downloadPDFFile

GENERATED_IMAGE_RESOLUTION = 300
NOTIFICATIONS_FILES_PATH = 'data/data/notificationsFiles/'

def clearNotificationsFilesDir():
    if (os.path.isdir(NOTIFICATIONS_FILES_PATH)):
        shutil.rmtree(NOTIFICATIONS_FILES_PATH)
    os.mkdir(NOTIFICATIONS_FILES_PATH)

def generateNotificationFiles(filesNamePattern, notificationURL):
    notificationPDF = downloadPDFFile(notificationURL,
                                      NOTIFICATIONS_FILES_PATH,
                                      filesNamePattern + '.pdf')
    imagesFileNamePattern = filesNamePattern + '_page-'
    imagesPathPattern = NOTIFICATIONS_FILES_PATH + imagesFileNamePattern

    # cause of memory leak during verification
    with pdfplumber.open(notificationPDF) as PDF:
        numOfPages = len(PDF.pages)
        for page in PDF.pages:
            imagePath = imagesPathPattern + str(page.page_number) + '.png'
            image = page.to_image(resolution = GENERATED_IMAGE_RESOLUTION)
            image.save(imagePath)
    return {'numOfPages': numOfPages, 'imagesFileNamePattern': imagesFileNamePattern}

def configureNotificationsFiles(notificationsLinks):
    NOTIFICATIONS = dict()

    clearNotificationsFilesDir()
    fileId = 1
    for notification in notificationsLinks:
        filesNamePattern = 'FILE-' + str(fileId)
        result = generateNotificationFiles(filesNamePattern, notification['URL'])
        notificationInfo = {'URL': notification['URL'],
                            'IMAGES_FILE_NAME_PATTERN': result['imagesFileNamePattern'],
                            'NUM_OF_PAGES': result['numOfPages']}
        NOTIFICATIONS[notification['name']] = notificationInfo
        fileId = fileId + 1

    setNotifications(NOTIFICATIONS)