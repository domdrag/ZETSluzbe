from distutils.dir_util import copy_tree 

# Can update files produce some garbage which won't be removed by repair?
def repairAllFiles():
    copy_tree('data/backup',
              'data')
