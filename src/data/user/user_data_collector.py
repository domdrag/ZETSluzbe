from datetime import date

from src.data.user.utils.user_collect_phase import UserCollectPhase

from src.data.share.dropbox_share import (isDropboxSynchronizationNeeded,
                                          dropbboxSynchronization)
from src.data.share.error_manager import (unsetUpdateSuccessful,
                                                 setUpdateSuccessful)
from src.data.share.get_warning_message_info import (
    getWarningMessageInfo
    )
from src.data.share.update_backup_dir import updateBackupDir
from src.data.share.repair_all_files import repairAllFiles
from src.share.trace import TRACE

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
                          'errorMessage': '',
                          'warningMessage': '',
                          'warningMessageColor': ''}
        try:
            if self.phase == cp.DROPBOX_SYNCHRONIZATION:
                TRACE('DROPBOX_SYNCHRONIZATION')
                unsetUpdateSuccessful()
                if isDropboxSynchronizationNeeded():
                    dropbboxSynchronization()
                    returnMessage['message'] = 'Postavljanje oglasne poruke'
                else:
                    setUpdateSuccessful()
                    returnMessage['finished'] = True
                
            elif self.phase == cp.SET_WARNING_MESSAGE:
                TRACE('SET_WARNING_MESSAGE')
                warningMessageInfo = getWarningMessageInfo()
                self.warningMessage = warningMessageInfo['message']
                self.warningMessageColor = warningMessageInfo['color']
                returnMessage['message'] = 'Kopiranje sluzbi'

            elif self.phase == cp.UPDATE_BACKUP_DIRECTORY:
                # must not fail by canon
                TRACE('UPDATE_BACKUP_DIRECTORY')
                setUpdateSuccessful() # must go before so backup gets it
                updateBackupDir() # must not fail by canon
                returnMessage['success'] = True
                returnMessage['finished'] = True
                returnMessage['message'] = 'Sluzbe azurirane!'
                returnMessage['warningMessage'] = self.warningMessage
                returnMessage['warningMessageColor'] = self.warningMessageColor
                
        except Exception as e:
            TRACE(e)
            repairAllFiles()
            return {'success': False,
                    'error': True,
                    'finished': True,
                    'message': 'GRESKA! Popravljanje dokumenata..\n',
                    'errorMessage': str(e),
                    'warningMessage': '',
                    'warningMessageColor': ''}
        self.phase = cp(self.phase.value + 1)
        if self.phase == cp.END:
            self.phase = cp.DROPBOX_SYNCHRONIZATION
        return returnMessage


