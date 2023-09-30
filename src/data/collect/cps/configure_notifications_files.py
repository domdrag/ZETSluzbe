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

def generateNotificationFiles(notificationName, notificationURL):
    notificationPDF = downloadPDFFile(notificationURL,
                                      NOTIFICATIONS_FILES_PATH,
                                      notificationName + '.pdf')

    PDF = pdfplumber.open(notificationPDF)
    imagePathPattern = NOTIFICATIONS_FILES_PATH + notificationName + '_page-'
    for page in PDF.pages:
        imagePath = imagePathPattern + str(page.page_number) + '.png'
        image = page.to_image(resolution = GENERATED_IMAGE_RESOLUTION)
        image.save(imagePath)
    return {'numOfPages': len(PDF.pages)}

def configureNotificationsFiles(notificationsLinks):
    NOTIFICATIONS = dict()

    clearNotificationsFilesDir()
    for notification in notificationsLinks:
        result = generateNotificationFiles(notification['name'], notification['URL'])
        NOTIFICATIONS[notification['name']] = {'URL': notification['URL'],
                                               'NUM_OF_PAGES': result['numOfPages']}

    setNotifications(NOTIFICATIONS)