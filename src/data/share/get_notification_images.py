import pdfplumber
import os

from src.data.share.download_pdf_file import downloadPDFFile
from src.share.trace import TRACE

GENERATED_IMAGE_RESOLUTION = 300

def generateImages(notificationPDF, imagePathPattern):
    imagesPathList = []

    PDF = pdfplumber.open(notificationPDF)
    for page in PDF.pages:
        imagePath = imagePathPattern + str(page.page_number) + '.png'
        image = page.to_image(resolution = GENERATED_IMAGE_RESOLUTION)
        image.save(imagePath)
        imagesPathList.append(imagePath)

    return imagesPathList

def getNotificationImages(notificationName, notificationLink):
    tempDirPath = 'data/temp/'
    if (not os.path.isdir(tempDirPath)):
        os.mkdir(tempDirPath)

    imagePathPattern = tempDirPath + notificationName + '_page-'
    imagesPathList = []

    imageNumber = 1
    while (os.path.isfile(imagePath := imagePathPattern +
                                       str(imageNumber) +
                                       '.png')):
        TRACE('(NOTIFICATION)_IMAGE_FOUND')
        imagesPathList.append(imagePath)
        imageNumber += 1

    # assume all required .pngs are generated if found any
    if (not imagesPathList):
        TRACE('(NOTIFICATION)_GENERATING_IMAGES')
        notificationPDF = downloadPDFFile(notificationLink,
                                          tempDirPath,
                                          'notification.pdf')
        imagesPathList = generateImages(notificationPDF, imagePathPattern)

    return imagesPathList