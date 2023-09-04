import shutil

def restoreWarnings():
    shutil.copyfile('data/backup/data/warnings.txt',
                    'data/data/warnings.txt')