from distutils.dir_util import copy_tree
import shutil

def updateBackupDir():
    copy_tree('data/data', 'data/backup/data')
    shutil.copyfile('data/config.json', 'data/backup/config.json')

