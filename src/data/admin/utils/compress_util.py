import shutil

def compressData():
    shutil.make_archive('data/dropbox/data', 'zip', 'data/data')
    shutil.copyfile('data/data/last_record_date.txt',
                    'data/dropbox/last_record_date.txt')

    
