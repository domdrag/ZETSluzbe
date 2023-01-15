from distutils.dir_util import copy_tree
import shutil
import os

def updateCopyDir():
    files = os.listdir('data/all_services_by_driver_decrypted_copy')
    for file in files:
        os.remove(os.path.join('data/all_services_by_driver_decrypted_copy',
                               file))

    files = os.listdir('data/all_shifts_by_driver_decrypted_copy')
    for file in files:
        os.remove(os.path.join('data/all_shifts_by_driver_decrypted_copy',
                               file))

    shutil.copy2('data/last_record_date.txt', 'data/copy/last_record_date.txt') 
    shutil.copy2('data/warnings.txt', 'data/copy/warnings.txt')
    copy_tree('data/all_services_by_driver_decrypted',
              'data/all_services_by_driver_decrypted_copy')
    copy_tree('data/all_shifts_by_driver_decrypted',
              'data/all_shifts_by_driver_decrypted_copy')
