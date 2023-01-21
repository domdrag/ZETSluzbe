import shutil

def compressData():
    shutil.make_archive('data/data', 'zip', 'data/data')

def decompressData():
    shutil.unpack_archive('data/dropbox/data.zip', 'data/data')
    
