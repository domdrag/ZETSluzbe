import os

from src.data.share.decompress_services import decompressServicesFile
from src.share.filenames import CENTRAL_DATA_DIR

def getServices(offNum):
    servicesFile = str(offNum) + '.txt'
    filePath = CENTRAL_DATA_DIR + servicesFile
    decompressServicesFile(servicesFile)
    fileR = open(filePath, 'r', encoding='utf-8')
    services = fileR.readlines()
    fileR.close()
    os.remove(filePath)
    return services