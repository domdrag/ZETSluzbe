import sys
from distutils.dir_util import copy_tree

import src.data.share.config_manager as configManager
import src.share.trace as trace

# Can update files produce some garbage which won't be removed by repair?
def repairAllFiles():
    trace.TRACE('REPAIRING DATA AND CONFIG')
    try:
        # repairing data + config
        copy_tree('data/backup',
                  'data')
    except Exception as e:
        trace.TRACE(e)
        # if repair failed -> make sure data gets proper repair in the next run and crash the app
        # manual set needed because we don't know whether copy_tree copied backup config
        configManager.setConfig('UPDATE_SUCCESSFUL', 0)
        sys.exit()
    trace.TRACE('DATA AND CONFIG REPAIRED')