from distutils.dir_util import copy_tree

def repairAllFiles():
    copy_tree('data/backup',
              'data/data')
