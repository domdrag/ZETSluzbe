import os

from src.data.share.decompress_file import decompressServicesFile

CENTRAL_DATA_DIR = 'data/central_data/'

def getServices(offNum):
    servicesFile = str(offNum) + '.txt'
    filePath = CENTRAL_DATA_DIR + servicesFile
    decompressServicesFile(servicesFile)
    fileR = open(filePath, 'r', encoding='utf-8')
    services = fileR.readlines()
    fileR.close()
    os.remove(filePath)
    return services