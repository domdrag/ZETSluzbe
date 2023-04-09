from enum import Enum

class UserCollectPhase(Enum):
    DROPBOX_SYNCHRONIZATION = 0
    SET_WARNING_MESSAGE = 1
    UPDATE_BACKUP_DIRECTORY = 2 
    END = 3
