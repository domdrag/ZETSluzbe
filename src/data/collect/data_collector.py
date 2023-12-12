from datetime import date

from src.data.collect.cps.collect_phase_enum import CollectPhaseEnum
from src.data.collect.cps.dropbox_synchronizer import DropboxSynchronizer

from src.data.collect.utils.generate_URLs import generateURLs
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
from src.data.collect.cps.configure_days_and_week_schedule import configureDaysAndWeekSchedule
from src.data.collect.cps.extract_rules_by_driver import (
    extractRulesByDriverAndCalculateServicesHash
    )
from src.data.collect.cps.extract_rules import extractRules
from src.data.collect.cps.upload_data_to_dropbox import (
    uploadDataToDropbox
    )
from src.data.collect.cps.check_update_neeeded import checkUpdateNeeded
from src.data.collect.cps.prepare_data_for_transport import prepareDataForTransport
from src.data.collect.cps.upload_client_data import uploadClientData
from src.data.collect.cps.configure_notifications_files import configureNotificationsFiles
from src.data.manager.backup_manager import repairSystem, updateBackupDir
from src.data.manager.config_manager import setConfig, setNewConfiguration, loadConfig, getConfig
from src.data.manager.warning_messages_manager import WarningMessagesManager
from src.share.trace import TRACE
from src.share.asserts import ASSERT_THROW

cp = CollectPhaseEnum

class DataCollector:
    def __init__(self, queue):
        from src.data.manager.logs_manager import LogsManager
        LogsManager.activateLiveLogging(queue)
        TRACE('CONFIGURING_DATA_COLLECTOR')
        self.phase = cp(0)
        self.days = []
        self.workDayLinks = ''
        self.saturdayLinks = ''
        self.sundayLinks = ''
        self.specialDayLinks = ''
        self.notificationsLinks = ''
        self.mondayDate = date(2022, 1, 1)
        self.weekSchedule = ['W', 'W', 'W', 'W', 'W', 'W', 'W']
        self.servicesHash = None
        self.workDayFileNames = []
        self.canUseOldWorkDayResources = False
        self.skipOnlineSyncsDueTestConfig = False

        # check if test configuration activated - if so, load configuration
        self.config = getConfig()
        if (not self.config):
            # test configuration expected - loading configuration
            TRACE('LOADING CONFIGURATION - SHOULD ONLY OCCUR AT THE TEST VERIFICATION')
            loadConfig()
            self.config = getConfig()
            errorMessage = 'ERROR - UNLOADED CONFIG AT THE START OF NON-TEST DATA COLLECTION'
            ASSERT_THROW(self.config['ACTIVATED_TEST_PACK_NUM'], errorMessage)
            self.skipOnlineSyncsDueTestConfig = True

        # depends on whether test config is activated
        URLs = generateURLs(self.config)
        self.mainPageURL = URLs['mainPageURL']
        self.allServicesURL = URLs['allServicesURL']

        TRACE('DATA_COLLECTOR_CONFIGURED')
    
    def keepCollectingData(self):
        print('hi')
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
                dropboxSynchronizationNeeded = dropboxSynchronizer.isDropboxSynchronizationNeeded()

                if (self.skipOnlineSyncsDueTestConfig):
                    TRACE('TEST_PACK_NUM_ACTIVATED - dropbox synchronization not needed')
                elif (dropboxSynchronizationNeeded):
                    TRACE('PERFORMING_DROPBOX_SYNCHRONIZATION')
                    dropboxSynchronizer.dropbboxSynchronization()
                    TRACE('DROPBOX_SYNCHRONIZATION_DONE')
                else:
                    TRACE('DROPBOX_SYNCHRONIZATION_NOT_NEEDED')
                returnMessage['message'] = 'Konfiguracija dana i tjednog rasporeda'

            elif self.phase == cp.CONFIGURE_DAYS_AND_WEEK_SCHEDULE:
                TRACE('[CP] CONFIGURE_DAYS_AND_WEEK_SCHEDULE')
                result = configureDaysAndWeekSchedule(self.allServicesURL, self.weekSchedule, self.days)
                self.mondayDate = result['mondayDate']
                returnMessage['message'] = 'Citanje tjednih sluzbi'

            elif self.phase == cp.EXTRACT_RULES_BY_DRIVER:
                TRACE('[CP] EXTRACT_RULES_BY_DRIVER')
                result = extractRulesByDriverAndCalculateServicesHash()
                self.servicesHash = result['servicesHash']
                returnMessage['message'] = 'Odredivanje potrebe azuriranja'

            elif self.phase == cp.CHECK_UPDATE_NEEDED:
                TRACE('[CP] CHECKING_UPDATE_NEEDED')
                updateNeeded = checkUpdateNeeded(self.mondayDate, self.servicesHash)
                if not updateNeeded:
                    TRACE('UPDATE_NOT_PERFORMING')
                    setConfig('UPDATE_SUCCESSFUL', 1)
                    returnMessage['finished'] = True

                else:
                    TRACE('PERFORMING_UPDATE')
                    returnMessage['message'] = \
                                  'Brisanje potrebnih podataka'

            elif self.phase == cp.SEARCH_LINKS:
                TRACE('[CP] SEARCH_LINKS')
                foundLinks = searchLinks(self.mainPageURL)
                self.workDayLinks = foundLinks['workDay']
                self.saturdayLinks = foundLinks['saturday']
                self.sundayLinks = foundLinks['sunday']
                self.specialDayLinks = foundLinks['specialDay']
                self.notificationsLinks = foundLinks['notificationsLinks']
                returnMessage['message'] = 'Brisanje potrebnih podataka'

            elif self.phase == cp.DELETE_NECESSARY_DATA:
                TRACE('[CP] DELETE_NECESSARY_DATA')
                result = deleteNecessaryData(self.workDayLinks, self.specialDayLinks)
                self.canUseOldWorkDayResources = result['canUseOldWorkDayResources']
                TRACE('Old Work Day resources enabled: ' +
                      str(self.canUseOldWorkDayResources))
                returnMessage['message'] = 'Citanje svih sluzbi'
                
            elif self.phase == cp.EXTRACT_RULES:
                TRACE('[CP] EXTRACT_RULES')
                self.fileNames = extractRules(self.workDayLinks,
                                              self.saturdayLinks,
                                              self.sundayLinks,
                                              self.specialDayLinks,
                                              self.weekSchedule,
                                              self.mondayDate,
                                              self.canUseOldWorkDayResources)
                returnMessage['message'] = 'Spremanje tjednih sluzbi'
                
            elif self.phase == cp.ADD_DECRYPTED_SERVICES:
                TRACE('[CP] ADD_DECRYPTED_SERVICES')
                addDecryptedServices(self.days,
                                     self.weekSchedule,
                                     self.mondayDate,
                                     self.fileNames)
                returnMessage['message'] = 'Spremanje tjednih smjena'
                
            elif self.phase == cp.ADD_DECRYPTED_SHIFTS:
                TRACE('[CP] ADD_DECRYPTED_SHIFTS')
                addDecryptedShifts(self.days,
                                   self.weekSchedule,
                                   self.mondayDate,
                                   self.fileNames)
                returnMessage['message'] = \
                    'Konfiguracija notifikacija'

            elif self.phase == cp.CONFIGURE_NOTIFICATION_FILES:
                TRACE('[CP] CONFIGURE_NOTIFICATION_FILES')
                configureNotificationsFiles(self.notificationsLinks)
                returnMessage['message'] = 'Spremanje nove konfiguracije'

            # NEXT ORDER EXPLANATION: in case anything fails, we must have
            # have a backup ready -> last step must be updating the backup.
            elif self.phase == cp.SET_NEW_CONFIG_AND_WARNINGS:
                TRACE('[CP] SET_NEW_CONFIG_AND_WARNINGS')
                mondayDateList = [self.mondayDate.year,
                                  self.mondayDate.month,
                                  self.mondayDate.day]
                setNewConfiguration(mondayDateList, self.servicesHash)
                WarningMessagesManager.setWarningMessages()
                returnMessage['message'] =  'Pripremanje podataka za transport'

            elif self.phase == cp.PREPARE_DATA_FOR_TRANSPORT:
                TRACE('[CP] PREPARE_DATA_FOR_TRANSPORT')
                prepareDataForTransport()
                returnMessage['message'] = \
                    'Ucitavanje sluzbi na Github'

            elif self.phase == cp.UPLOAD_CLIENT_DATA:
                TRACE('[CP] UPLOAD_CLIENT_DATA')
                if (not self.skipOnlineSyncsDueTestConfig):
                    uploadClientData()
                    TRACE('DATA_UPLOADED_TO_GITHUB_SUCCESSFULLY')
                else:
                    TRACE('TEST_PACK_NUM_ACTIVATED - skipping uploading client data')
                returnMessage['message'] = \
                    'Ucitavanje sluzbi na Dropbox'

            elif self.phase == cp.UPLOAD_DATA_TO_DROPBOX:
                TRACE('[CP] UPLOAD_DATA_TO_DROPBOX')
                if (not self.skipOnlineSyncsDueTestConfig):
                    uploadDataToDropbox()
                    TRACE('DATA_UPLOADED_TO_DROPBOX_SUCCESSFULLY')
                else:
                    TRACE('TEST_PACK_NUM_ACTIVATED - skipping uploading author data')
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
            WarningMessagesManager.clearWarningMessages()

            return {'success': False,
                    'error': True,
                    'finished': True,
                    'message': 'GRESKA! Popravljanje dokumenata..\n',
                    'errorMessage': str(e)}

        self.phase = cp(self.phase.value + 1)
        return returnMessage

