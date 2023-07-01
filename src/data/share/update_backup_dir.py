from distutils.dir_util import copy_tree
import shutil

def updateBackupConfig():
    shutil.copyfile('data/config.json', 'data/backup/config.json')

def updateBackupDir():
    updateBackupConfig()
    copy_tree('data/data', 'data/backup/data')

