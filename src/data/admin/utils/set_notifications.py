import json
import os
import shutil
import pdfplumber

from src.data.share.download_pdf_file import downloadPDFFile

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

def setNotifications(notifications):
    NOTIFICATIONS = dict()

    clearNotificationsFilesDir()
    for notification in notifications:
        NOTIFICATIONS[notification['name']] = {'URL': notification['URL']}
        generateNotificationFiles(notification['name'], notification['URL'])

    with open('data/data/notifications.json', 'w', encoding='utf-8') as notificationsFile:
        json.dump(NOTIFICATIONS, notificationsFile, indent = 3)