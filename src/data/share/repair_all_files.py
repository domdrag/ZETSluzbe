#from distutils.dir_util import copy_tree 
import shutilt # distutils has been deprecated in 3.10 or 3.12

def repairAllFiles():
    shutil.copytree('data/backup',
                    'data/data')

'''
def repairAllFiles():
    copy_tree('data/backup',
              'data/data')'''
