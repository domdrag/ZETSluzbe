from datetime import date

from src.data.user.utils.user_collect_phase import UserCollectPhase

from src.data.share.dropbox_share import (isDropboxSynchronizationNeeded,
                                          dropbboxSynchronization)
from src.data.share.get_warning_message_info import (
    getWarningMessageInfo
    )
from src.data.share.update_backup_dir import updateBackupDir
from src.data.share.repair_all_files import repairAllFiles
from src.share.trace import TRACE
from src.data.share.config_manager import setConfig

cp = UserCollectPhase

class UserDataCollector:
    phase = cp.DROPBOX_SYNCHRONIZATION
    warningMessage = ''
    warningMessageColor = ''
    
    def keepCollectingData(self):
        returnMessage = { 'success': False,
                          'error': False,
                          'finished': False,
                          'message': '',
                          'errorMessage': ''}
        try:
            if self.phase == cp.DROPBOX_SYNCHRONIZATION:
                TRACE('DROPBOX_SYNCHRONIZATION')
                setConfig('UPDATE_SUCCESSFUL', 0)
                if isDropboxSynchronizationNeeded():
                    dropbboxSynchronization()
                    returnMessage['message'] = 'Postavljanje oglasne poruke'
                else:
                    setConfig('UPDATE_SUCCESSFUL', 1)
                    returnMessage['finished'] = True

            elif self.phase == cp.UPDATE_BACKUP_DIRECTORY:
                TRACE('UPDATE_BACKUP_DIRECTORY')
                # must go before so backup gets it
                setConfig('UPDATE_SUCCESSFUL', 1)
                updateBackupDir()
                returnMessage['success'] = True
                returnMessage['finished'] = True
                returnMessage['message'] = 'Sluzbe azurirane!'
                
        except Exception as e:
            TRACE(e)
            repairAllFiles()
            return {'success': False,
                    'error': True,
                    'finished': True,
                    'message': 'GRESKA! Popravljanje dokumenata..\n',
                    'errorMessage': str(e)}
        self.phase = cp(self.phase.value + 1)
        if self.phase == cp.END:
            self.phase = cp.DROPBOX_SYNCHRONIZATION
        return returnMessage


