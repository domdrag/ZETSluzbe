from datetime import date

from src.data.collect.cps.collect_phase_enum import CollectPhaseEnum
from src.data.collect.cps.dropbox_synchronizer import DropboxSynchronizer

from src.data.collect.cps.add_decrypted_services import (
    addDecryptedServices
    )
from src.data.collect.cps.add_decrypted_shifts import (
    addDecryptedShifts
    )
from src.data.collect.cps.delete_necessary_data import (
    deleteNecessaryData
    )
from src.data.collect.cps.search_links import searchLinks
from src.data.collect.cps.configure_days import configureDays
from src.data.collect.cps.extract_rules_by_driver import (
    extractRulesByDriver
    )
from src.data.collect.cps.extract_rules import extractRules
from src.data.collect.cps.upload_data_to_dropbox import (
    uploadDataToDropbox
    )
from src.data.collect.cps.configure_missing_services import configureMissingServices
from src.data.collect.cps.check_update_neeeded import checkUpdateNeeded
from src.data.collect.cps.prepare_data_for_transport import prepareDataForTransport
from src.data.collect.cps.upload_client_data import uploadClientData
from src.data.collect.cps.configure_notifications_files import configureNotificationsFiles
from src.data.manager.backup_manager import repairSystem, updateBackupDir, restoreWarnings
from src.data.manager.config_manager import setConfig, setNewConfiguration, loadConfig
from src.share.trace import TRACE

cp = CollectPhaseEnum

class DataCollector:
    phase = cp(0)
    days = []
    workDayLinks = ''
    saturdayLinks = ''
    sundayLinks = ''
    notificationsLinks = ''
    mondayDate = date(2022,1,1)
    weekSchedule = ['W','W','W','W','W','W','W']
    synchronizationNeeded = False
    warningMessage = ''
    warningMessageColor = ''
    updateCause = None
    missingServices = None
    servicesHash = None
    workDayFileNames = []
    
    def keepCollectingData(self):
        returnMessage = { 'success': False,
                          'error': False,
                          'finished': False,
                          'message': '',
                          'errorMessage': ''}
        try:
            if self.phase == cp.DROPBOX_SYNCHRONIZATION:
                TRACE('[CP] DROPBOX_SYNCHRONIZATION')
                setConfig('UPDATE_SUCCESSFUL', 0)
                dropboxSynchronizer = DropboxSynchronizer()
                if dropboxSynchronizer.isDropboxSynchronizationNeeded():
                    TRACE('PERFORMING_DROPBOX_SYNCHRONIZATION')
                    self.synchronizationNeeded = True
                    dropboxSynchronizer.dropbboxSynchronization()
                    TRACE('DROPBOX_SYNCHRONIZATION_DONE')
                returnMessage['message'] = 'Trazenje linkova'
                
            elif self.phase == cp.SEARCH_LINKS:
                TRACE('[CP] SEARCH_LINKS')
                foundLinks = searchLinks()
                self.workDayLinks = foundLinks['workDay']
                self.saturdayLinks = foundLinks['saturday']
                self.sundayLinks = foundLinks['sunday']
                self.notificationsLinks = foundLinks['notifications']
                returnMessage['message'] = 'Konfiguracija notifikacija'

            elif self.phase == cp.CONFIGURE_NOTIFICATION_FILES:
                TRACE('[CP] CONFIGURE_NOTIFICATION_FILES')
                configureNotificationsFiles(self.notificationsLinks)
                returnMessage['message'] = 'Setiranje dana'

            elif self.phase == cp.CONFIGURE_DAYS:
                TRACE('[CP] CONFIGURE_DAYS')
                self.mondayDate = configureDays(self.days)
                returnMessage['message'] = 'Citanje tjednih sluzbi'

            elif self.phase == cp.EXTRACT_RULES_BY_DRIVER:
                TRACE('[CP] EXTRACT_RULES_BY_DRIVER')
                result = extractRulesByDriver(self.weekSchedule, self.mondayDate)
                self.servicesHash = result['servicesHash']
                returnMessage['message'] = 'Pretraga nedostajucih sluzbi'

            elif self.phase == cp.CONFIGURE_MISSING_SERVICES:
                TRACE('[CP] CONFIGURE_MISSING_SERVICES')
                self.missingServices = configureMissingServices()
                returnMessage['message'] = 'Odredivanje potrebe azuriranja'

            elif self.phase == cp.CHECK_UPDATE_NEEDED:
                TRACE('[CP] CHECKING_UPDATE_NEEDED')
                result = checkUpdateNeeded(self.mondayDate,
                                           self.missingServices,
                                           self.servicesHash,
                                           self.synchronizationNeeded)
                updateNeeded = result['updateNeeded']
                self.updateCause = result['updateCause']
                if not updateNeeded:
                    TRACE('UPDATE_NOT_PERFORMING')
                    # REMARK - if services haven't been added in Friday yet,
                    # but admin still had synch with dropbox (he was inactive
                    # for at least a week) we still got 'Sluzbe azurirane'
                    # which may be misleading 
                    if self.synchronizationNeeded:
                        # will be + 1 after so UPDATE_BACKUP_DIRECTORY
                        self.phase = cp.UPLOAD_DATA_TO_DROPBOX 
                        returnMessage['message'] = 'Stvaranje sigurnosne kopije'
                    else:
                        restoreWarnings()
                        setConfig('UPDATE_SUCCESSFUL', 1)
                        returnMessage['finished'] = True
                else:
                    TRACE('PERFORMING_UPDATE')
                    returnMessage['message'] = \
                                  'Brisanje potrebnih podataka'

            elif self.phase == cp.DELETE_NECESSARY_DATA:
                TRACE('[CP] DELETE_NECESSARY_DATA')
                deleteNecessaryData()
                returnMessage['message'] = 'Citanje svih sluzbi'
                
            elif self.phase == cp.EXTRACT_RULES:
                TRACE('[CP] EXTRACT_RULES')
                fileNames = extractRules(self.workDayLinks,
                                         self.saturdayLinks,
                                         self.sundayLinks)
                self.workDayFileNames = fileNames['workDay']
                returnMessage['message'] = 'Spremanje tjednih sluzbi'
                
            elif self.phase == cp.ADD_DECRYPTED_SERVICES:
                TRACE('[CP] ADD_DECRYPTED_SERVICES')
                addDecryptedServices(self.days,
                                     self.weekSchedule,
                                     self.missingServices,
                                     self.updateCause,
                                     self.mondayDate,
                                     self.workDayFileNames)
                returnMessage['message'] = 'Spremanje tjednih smjena'
                
            elif self.phase == cp.ADD_DECRYPTED_SHIFTS:
                TRACE('[CP] ADD_DECRYPTED_SHIFTS')
                addDecryptedShifts(self.days,
                                   self.weekSchedule,
                                   self.missingServices,
                                   self.updateCause,
                                   self.mondayDate,
                                   self.workDayFileNames)
                returnMessage['message'] = \
                    'Spremanje nove konfiguracije'

            # NEXT ORDER EXPLANATION: in case anything fails, we must have
            # have a backup ready -> last step must be updating the backup.
            elif self.phase == cp.SET_NEW_CONFIG:
                TRACE('[CP] SET_NEW_CONFIG')
                mondayDateList = [self.mondayDate.year,
                                  self.mondayDate.month,
                                  self.mondayDate.day]
                setNewConfiguration(mondayDateList, self.missingServices, self.servicesHash)
                returnMessage['message'] =  'Pripremanje podataka za transport'

            elif self.phase == cp.PREPARE_DATA_FOR_TRANSPORT:
                TRACE('[CP] PREPARE_DATA_FOR_TRANSPORT')
                prepareDataForTransport()
                returnMessage['message'] = \
                    'Ucitavanje sluzbi na Github'

            elif self.phase == cp.UPLOAD_CLIENT_DATA:
                TRACE('[CP] UPLOAD_CLIENT_DATA')
                uploadClientData()
                returnMessage['message'] = \
                    'Ucitavanje sluzbi na Dropbox'

            elif self.phase == cp.UPLOAD_DATA_TO_DROPBOX:
                TRACE('[CP] UPLOAD_DATA_TO_DROPBOX')
                # dodaj mockan UPD_SUCC da se salje
                uploadDataToDropbox()
                TRACE('DATA_UPLOADED_TO_DROPBOX_SUCCESSFULLY')
                returnMessage['message'] = 'Stvaranje sigurnosne kopije'
            
            elif self.phase == cp.UPDATE_BACKUP_DIRECTORY:
                # must not fail by canon
                TRACE('[CP] UPDATE_BACKUP_DIRECTORY')
                # must go before updateBackupDir() so backup gets it
                setConfig('UPDATE_SUCCESSFUL', 1)
                updateBackupDir() 
                returnMessage['success'] = True
                returnMessage['finished'] = True
                returnMessage['message'] = 'Sluzbe azurirane!'
                TRACE('SERVICES_UPDATE_FINISHED_SUCCESSFULLY')
                
        except Exception as e:
            TRACE(e)
            repairSystem()
            return {'success': False,
                    'error': True,
                    'finished': True,
                    'message': 'GRESKA! Popravljanje dokumenata..\n',
                    'errorMessage': str(e)}

        self.phase = cp(self.phase.value + 1)
        return returnMessage


