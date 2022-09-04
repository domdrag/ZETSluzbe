import os
from distutils.dir_util import copy_tree

def repairFiles():
    files = os.listdir('./services')
    for file in files:
        os.remove(os.path.join('./services', file))

    files = os.listdir('./shifts')
    for file in files:
        os.remove(os.path.join('./shifts', file))

    copy_tree('./servicesCopy', './services')
    copy_tree('./shiftsCopy', './shifts')

def updateCopyDir():
    files = os.listdir('./servicesCopy')
    for file in files:
        os.remove(os.path.join('./servicesCopy', file))

    files = os.listdir('./shiftsCopy')
    for file in files:
        os.remove(os.path.join('./shiftsCopy', file))

    copy_tree('./services', './servicesCopy')
    copy_tree('./shifts', './shiftsCopy')
