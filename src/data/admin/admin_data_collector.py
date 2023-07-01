from datetime import date

from src.data.admin.utils.admin_collect_phase import AdminCollectPhase

from src.data.admin.services_decrypted.write_decrypted_services import (
    writeDecryptedServices
    )
from src.data.admin.shifts_decrypted.write_decrypted_shifts import (
    writeDecryptedShifts
    )
from src.data.admin.utils.delete_necessary_data import (
    deleteNecessaryData
    )
from src.data.admin.utils.search_links import searchLinks  
from src.data.admin.utils.set_days import setDays
from src.data.admin.utils.set_last_record import setLastRecord
from src.data.admin.rules.extract_rules_by_driver import (
    extractRulesByDriver
    )
from src.data.admin.rules.extract_rules import extractRules
from src.data.admin.utils.upload_data_to_dropbox import (
    uploadDataToDropbox
    )
from src.data.share.dropbox_share import (isDropboxSynchronizationNeeded,
                                          dropbboxSynchronization)
from src.data.share.get_warning_message_info import (
    getWarningMessageInfo
    )
from src.data.share.repair_all_files import repairAllFiles
from src.share.trace import TRACE
from src.data.share.config_manager import setConfig
from src.data.share.update_backup_dir import updateBackupDir

cp = AdminCollectPhase

class AdminDataCollector:
    phase = cp.DROPBOX_SYNCHRONIZATION
    days = []
    workDayURL = ''
    saturdayURL = ''
    sundayURL = ''
    mondayDate = date(2022,1,1)
    weekSchedule = ['W','W','W','W','W','W','W']
    synchronizationNeeded = False
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
                    self.synchronizationNeeded = True
                    dropbboxSynchronization()                
                returnMessage['message'] = 'Trazenje linkova'
                
            elif self.phase == cp.SEARCH_LINKS:
                TRACE('SEARCH_LINKS')
                foundLinks = searchLinks()
                self.workDayURL = foundLinks['workDay']
                self.saturdayURL = foundLinks['saturday']
                self.sundayURL = foundLinks['sunday']
                returnMessage['message'] = 'Provjera novih sluzbi'

            elif self.phase == cp.SET_DAYS:
                TRACE('SET_DAYS')
                result = setDays(self.days)
                updateNeeded = result['updateNeeded']
                if not updateNeeded:
                    # REMARK - if services haven't been added in Friday yet,
                    # but admin still had synch with dropbox (he was inactive
                    # for at least a week) we still got 'Sluzbe azurirane'
                    # which may be misleading 
                    if self.synchronizationNeeded:
                        # will be + 1 after so SET_WARNING_MESSAGE
                        self.phase = cp.UPLOAD_DATA_TO_DROPBOX 
                        returnMessage['message'] = 'Stvaranje sigurnosne kopije'
                    else:
                        setConfig('UPDATE_SUCCESSFUL', 1)
                        returnMessage['finished'] = True
                else:
                    self.mondayDate = result['mondayDate']
                    returnMessage['message'] = \
                                  'Brisanje potrebnih podataka'
                
            elif self.phase == cp.DELETE_NECESSARY_DATA:
                TRACE('DELETE_NECESSARY_DATA')
                deleteNecessaryData()
                returnMessage['message'] = 'Citanje tjednih sluzbi'
                    
            elif self.phase == cp.EXTRACT_RULES_BY_DRIVER:
                TRACE('EXTRACT_RULES_BY_DRIVER')
                extractRulesByDriver(self.weekSchedule, self.mondayDate)
                returnMessage['message'] = 'Citanje svih sluzbi'
                
            elif self.phase == cp.EXTRACT_RULES:
                TRACE('EXTRACT_RULES')
                extractRules(self.workDayURL,
                             self.saturdayURL,
                             self.sundayURL)
                returnMessage['message'] = 'Spremanje tjednih sluzbi'
                
            elif self.phase == cp.WRITE_DECRYPTED_SERVICES:
                TRACE('WRITE_DECRYPTED_SERVICES')
                writeDecryptedServices(self.days, self.weekSchedule)
                returnMessage['message'] = 'Spremanje tjednih smjena'
                
            elif self.phase == cp.WRITE_DECRYPTED_SHIFTS:
                TRACE('WRITE_DECRYPTED_SHIFTS')
                writeDecryptedShifts(self.days, self.weekSchedule)
                returnMessage['message'] = \
                              'Setiranje datuma zadnjeg zapisa'

            # NEXT ORDER EXPLANATION: in case anything fails, we must have
            # have a backup ready -> last step must be updating the backup.
            elif self.phase == cp.SET_LAST_RECORD:
                TRACE('SET_LAST_RECORD')
                setLastRecord(self.mondayDate)
                returnMessage['message'] = 'Ucitavanje sluzbi na Internet'

            elif self.phase == cp.UPLOAD_DATA_TO_DROPBOX:
                TRACE('UPLOAD_DATA_TO_DROPBOX')
                uploadDataToDropbox()
                returnMessage['message'] = 'Stvaranje sigurnosne kopije'
            
            elif self.phase == cp.UPDATE_BACKUP_DIRECTORY:
                # must not fail by canon
                TRACE('UPDATE_BACKUP_DIRECTORY')
                # must go first so backup gets it
                setConfig('UPDATE_SUCCESSFUL', 1)
                updateBackupDir() 
                returnMessage['success'] = True
                returnMessage['finished'] = True
                returnMessage['message'] = 'Sluzbe azurirane!'
            '''
            elif self.phase == cp.SET_WARNING_MESSAGE:
                TRACE('SET_WARNING_MESSAGE')
                warningMessageInfo = getWarningMessageInfo()
                self.warningMessage = warningMessageInfo['message']
                self.warningMessageColor = warningMessageInfo['color']
                returnMessage['message'] = 'Kopiranje sluzbi'
                '''
                
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
            self.phase = cp.SEARCH_LINKS
        return returnMessage


