from distutils.dir_util import copy_tree
import os

def repairFiles():
    files = os.listdir('data/all_services_by_driver_decrypted')
    for file in files:
        os.remove(os.path.join('data/all_services_by_driver_decrypted', file))

    files = os.listdir('data/all_shifts_by_driver_decrypted')
    for file in files:
        os.remove(os.path.join('data/all_shifts_by_driver_decrypted', file))

    copy_tree('data/copy', 'data')
    copy_tree('data/all_services_by_driver_decrypted_copy',
              'data/all_services_by_driver_decrypted')
    copy_tree('data/all_shifts_by_driver_decrypted_copy',
              'data/all_shifts_by_driver_decrypted')
