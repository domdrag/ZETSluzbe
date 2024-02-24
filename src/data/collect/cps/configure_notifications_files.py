import os
import shutil
import pdfplumber

from src.data.manager.notifications_manager import setNotifications
from src.data.collect.cps.utils.download_pdf_file import downloadPDFFile
from src.share.filenames import NOTIFICATIONS_FILES_DIR
from src.share.trace import TRACE

GENERATED_IMAGE_RESOLUTION = 300

def clearNotificationsFilesDir():
    if (os.path.isdir(NOTIFICATIONS_FILES_DIR)):
        shutil.rmtree(NOTIFICATIONS_FILES_DIR)
    os.mkdir(NOTIFICATIONS_FILES_DIR)

def generateNotificationFiles(filesNamePattern, notificationURL):
    imagesFileNamePattern = filesNamePattern + '_page-'
    imagesPathPattern = NOTIFICATIONS_FILES_DIR + imagesFileNamePattern
    try:
        notificationPDF = downloadPDFFile(notificationURL,
                                          NOTIFICATIONS_FILES_DIR,
                                          filesNamePattern + '.pdf')

        # cause of memory leak during verification
        with pdfplumber.open(notificationPDF) as PDF:
            numOfPages = len(PDF.pages)
            for page in PDF.pages:
                imagePath = imagesPathPattern + str(page.page_number) + '.png'
                image = page.to_image(resolution = GENERATED_IMAGE_RESOLUTION)
                image.save(imagePath)
    except Exception as e:
        # Should be the case when there is no PDF file uploaded for a notification.
        # We don't want to terminate the update, so we just keep going.
        TRACE('Error occured during generating following notification file: ' +
              filesNamePattern + '\nReason: '+ str(e))
        numOfPages = 0

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