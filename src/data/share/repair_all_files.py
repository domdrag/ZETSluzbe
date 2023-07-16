from distutils.dir_util import copy_tree
# from src.data.share.config_manager import setConfig

# Can update files produce some garbage which won't be removed by repair?
def repairAllFiles():
    # CAN'T USE TRACE BECAUSE OF CIRCULAR IMPORT
    print('REPAIRING DATA')
    copy_tree('data/backup',
              'data')
    '''
    try:
        copy_tree('data/backup',
                  'data')
    except Exception as e:
        print(e)
        # if repair failed -> app crash and we want to make sure data gets proper repair
        setConfig('UPDATE_SUCCESSFUL',0)'''

    print('DATA REPAIRED')
