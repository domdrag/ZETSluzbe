from datetime import date

from src.data.collect.cps.collect_phase_enum import CollectPhaseEnum
from src.data.collect.cps.collect_phase_enum import COLLECT_PHASE_OUTPUT_MESSAGE_MAP

from src.data.collect.utils.setup_data import initializeDataForUpdate, finishDataUpdate
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
from src.data.manager.backup_manager import updateBackupDir
from src.data.manager.config_manager import ConfigManager
from src.data.manager.warning_messages_manager import WarningMessagesManager
import src.data.data_handler as dataHandler
from src.share.trace import TRACE
from src.share.asserts import ASSERT_THROW

cp = CollectPhaseEnum
STARTING_OUTPUT_MESSAGE = COLLECT_PHASE_OUTPUT_MESSAGE_MAP[cp(0)]

class DataCollector:
    def __init__(self):
        TRACE('CONFIGURING_DATA_COLLECTOR')
        initializeDataForUpdate()

        self.phase = cp(0)
        self.dataModified = False
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
        self.dropboxSynchronizationNeeded = False
        self.canUseOldWorkDayResources = False
        self.skipOnlineSyncsDueToTestConfig = False

        if (ConfigManager.getConfig('ACTIVATED_TEST_PACK_NUM')):
            self.skipOnlineSyncsDueToTestConfig = True

        URLs = generateURLs()
        self.mainPageURL = URLs['mainPageURL']
        self.allServicesURL = URLs['allServicesURL']

        TRACE('DATA_COLLECTOR_CONFIGURED')
    
    def keepCollectingData(self):
        returnMessage = { 'success': False,
                          'error': False,
                          'finished': False,
                          'message': '',
                          'errorMessage': ''}
        try:
            if self.phase == cp.CONFIGURE_DAYS_AND_WEEK_SCHEDULE:
                TRACE('[CP] CONFIGURE_DAYS_AND_WEEK_SCHEDULE')
                result = configureDaysAndWeekSchedule(self.allServicesURL, self.weekSchedule, self.days)
                self.mondayDate = result['mondayDate']

            elif self.phase == cp.EXTRACT_RULES_BY_DRIVER:
                TRACE('[CP] EXTRACT_RULES_BY_DRIVER')
                result = extractRulesByDriverAndCalculateServicesHash()
                self.servicesHash = result['servicesHash']

            elif self.phase == cp.CHECK_UPDATE_NEEDED:
                TRACE('[CP] CHECKING_UPDATE_NEEDED')
                updateNeeded = checkUpdateNeeded(self.mondayDate, self.servicesHash)
                if not updateNeeded:
                    TRACE('UPDATE_NOT_PERFORMING')
                    if (self.dropboxSynchronizationNeeded):
                        self.dataModified = True

                    self.phase = cp.END

                else:
                    TRACE('PERFORMING_UPDATE')

            elif self.phase == cp.SEARCH_LINKS:
                TRACE('[CP] SEARCH_LINKS')
                foundLinks = searchLinks(self.mainPageURL)
                self.workDayLinks = foundLinks['workDay']
                self.saturdayLinks = foundLinks['saturday']
                self.sundayLinks = foundLinks['sunday']
                self.specialDayLinks = foundLinks['specialDay']
                self.notificationsLinks = foundLinks['notificationsLinks']

            elif self.phase == cp.DELETE_NECESSARY_DATA:
                TRACE('[CP] DELETE_NECESSARY_DATA')
                result = deleteNecessaryData(self.workDayLinks, self.specialDayLinks)
                self.canUseOldWorkDayResources = result['canUseOldWorkDayResources']
                TRACE('Old Work Day resources enabled: ' +
                      str(self.canUseOldWorkDayResources))
                
            elif self.phase == cp.EXTRACT_RULES:
                TRACE('[CP] EXTRACT_RULES')
                self.fileNames = extractRules(self.workDayLinks,
                                              self.saturdayLinks,
                                              self.sundayLinks,
                                              self.specialDayLinks,
                                              self.weekSchedule,
                                              self.mondayDate,
                                              self.canUseOldWorkDayResources)
                
            elif self.phase == cp.ADD_DECRYPTED_SERVICES:
                TRACE('[CP] ADD_DECRYPTED_SERVICES')
                addDecryptedServices(self.days,
                                     self.weekSchedule,
                                     self.mondayDate,
                                     self.fileNames)
                print('goto')
                import time
                time.sleep(100)
                
            elif self.phase == cp.ADD_DECRYPTED_SHIFTS:
                TRACE('[CP] ADD_DECRYPTED_SHIFTS')
                addDecryptedShifts(self.days,
                                   self.weekSchedule,
                                   self.mondayDate,
                                   self.fileNames)

            elif self.phase == cp.CONFIGURE_NOTIFICATION_FILES:
                TRACE('[CP] CONFIGURE_NOTIFICATION_FILES')
                configureNotificationsFiles(self.notificationsLinks)

            # NEXT ORDER EXPLANATION: in case anything fails, we must have
            # have a backup ready -> last step must be updating the backup.
            elif self.phase == cp.SET_NEW_CONFIG_AND_WARNINGS:
                TRACE('[CP] SET_NEW_CONFIG_AND_WARNINGS')
                mondayDateList = [self.mondayDate.year,
                                  self.mondayDate.month,
                                  self.mondayDate.day]
                ConfigManager.updateConfig('LAST_RECORD_DATE', mondayDateList)
                ConfigManager.updateConfig('SERVICES_HASH', self.servicesHash)
                WarningMessagesManager.setWarningMessages()

            elif self.phase == cp.PREPARE_DATA_FOR_TRANSPORT:
                TRACE('[CP] PREPARE_DATA_FOR_TRANSPORT')
                prepareDataForTransport()

            elif self.phase == cp.UPLOAD_CLIENT_DATA:
                TRACE('[CP] UPLOAD_CLIENT_DATA')
                if (not self.skipOnlineSyncsDueToTestConfig):
                    #uploadClientData()
                    TRACE('DATA_UPLOADED_TO_GITHUB_SUCCESSFULLY')
                else:
                    TRACE('TEST_PACK_NUM_ACTIVATED - skipping uploading client data')

            elif self.phase == cp.UPLOAD_DATA_TO_DROPBOX:
                TRACE('[CP] UPLOAD_DATA_TO_DROPBOX')
                if (not self.skipOnlineSyncsDueToTestConfig):
                    #uploadDataToDropbox()
                    TRACE('DATA_UPLOADED_TO_DROPBOX_SUCCESSFULLY')
                else:
                    TRACE('TEST_PACK_NUM_ACTIVATED - skipping uploading author data')
                self.dataModified = True
                
        except Exception as e:
            TRACE(e)
            dataHandler.recoverData()
            ConfigManager.abandonUpdate()

            return {'success': False,
                    'error': True,
                    'finished': True,
                    'message': 'GRESKA! Popravljanje dokumenata..\n',
                    'errorMessage': str(e)}

        if (self.phase != cp.END):
            self.phase = cp(self.phase.value + 1)
            returnMessage['message'] = COLLECT_PHASE_OUTPUT_MESSAGE_MAP[self.phase]

        if (self.phase == cp.END):
            finishDataUpdate()

            if (self.dataModified):
                #updateBackupDir()
                returnMessage['success'] = True

            returnMessage['finished'] = True
            TRACE('SERVICES_UPDATE_FINISHED_SUCCESSFULLY')

        return returnMessage
