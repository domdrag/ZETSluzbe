import shutil

def compressData():
    shutil.make_archive('data/dropbox/data', 'zip', 'data/data')

def prepareDataForTransport():
    compressData()
    shutil.copyfile('data/config.json', 'data/dropbox/config.json')