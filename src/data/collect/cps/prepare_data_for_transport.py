import os
import shutil

CENTRAL_DATA_DIR = 'data/central_data/'
COMPRESSED_CENTRAL_DATA_NO_EXT = 'data/temp/central_data/'
COMPRESSED_CENTRAL_DATA = COMPRESSED_CENTRAL_DATA_NO_EXT + '.zip'

def compressCentralData():
    shutil.make_archive(COMPRESSED_CENTRAL_DATA_NO_EXT, 'zip', CENTRAL_DATA_DIR)

def prepareDataForTransport():
    if (os.path.isfile(COMPRESSED_CENTRAL_DATA)):
        os.remove(COMPRESSED_CENTRAL_DATA)
    compressCentralData()