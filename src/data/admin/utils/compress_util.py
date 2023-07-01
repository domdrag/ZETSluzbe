import shutil

from src.data.share.config_manager import getConfig

def compressData():
    shutil.make_archive('data/dropbox/data', 'zip', 'data/data')
    
    config = getConfig()
    lastRecordDate = config['LAST_RECORD_DATE']
    fileW = open('data/dropbox/last_record_date.txt', 'w', encoding='utf-8')
    fileW.write(f"{lastRecordDate}\n")
    fileW.close()

