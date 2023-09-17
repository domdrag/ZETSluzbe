import pdfplumber

from src.data.share.download_pdf_file import downloadPDFFile

GENERATED_IMAGE_RESOLUTION = 300
NOTIFICATIONS_FILES_PATH = 'data/data/notificationsFiles/'

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