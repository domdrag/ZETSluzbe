from enum import Enum

class UserCollectPhase(Enum):
    DROPBOX_SYNCHRONIZATION = 0
    UPDATE_BACKUP_DIRECTORY = 1 
    END = 2
