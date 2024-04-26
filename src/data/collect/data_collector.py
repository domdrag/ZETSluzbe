from datetime import date

from src.data.manager.config_manager import ConfigManager
from src.data.manager.warning_messages_manager import WarningMessagesManager
from src.data.manager.update_info_manager import UpdateInfoManager
from src.data.collect.cps.collect_phase_enum import CollectPhaseEnum

from src.data.collect.utils.generate_URLs import generateURLs
from src.data.collect.cps.github_synchronization import githubSynchronization
from src.data.collect.cps.add_decrypted_services import addDecryptedServices
from src.data.collect.cps.add_decrypted_shifts import addDecryptedShifts
from src.data.collect.cps.delete_necessary_data import deleteNecessaryData
from src.data.collect.cps.search_links import searchLinks
from src.data.collect.cps.configure_days_and_week_schedule import configureDaysAndWeekSchedule
from src.data.collect.cps.extract_rules_by_driver import extractRulesByDriverAndCalculateServicesHash
from src.data.collect.cps.extract_rules import extractRules
from src.data.collect.cps.check_update_neeeded import checkUpdateNeeded
from src.data.collect.cps.upload_data import uploadData
from src.data.collect.cps.configure_notifications_files import configureNotificationsFiles

from src.data.collect.cps.collect_phase_enum import COLLECT_PHASE_OUTPUT_MESSAGE_MAP
from src.share.trace import TRACE

cp = CollectPhaseEnum
STARTING_OUTPUT_MESSAGE = COLLECT_PHASE_OUTPUT_MESSAGE_MAP[cp(0)]

class DataCollector:
    def __init__(self):
        TRACE('CONFIGURING_DATA_COLLECTOR')
        ConfigManager.initiateDataUpdate()

        self.phase = cp(0)
        self.servicesHash = 0
        self.mondayDate = date(1,1,1)
        self.workDayLinks = []
        self.saturdayLinks = []
        self.sundayLinks = []
        self.specialDayLinks = []
        self.notificationsLinks = []
        self.days = []
        self.fileNames = []
        self.weekSchedule = ['W', 'W', 'W', 'W', 'W', 'W', 'W']
        self.canUseOldWorkDayResources = False
        self.canUseOldSaturdayResources = False
        self.canUseOldSundayResources = False
        self.skipOnlineSyncsDueToTestConfig = False
        self.missingServices = False

        if (ConfigManager.getConfig('ACTIVATED_TEST_PACK_NUM')):
            TRACE('ACTIVATED TEST PACK NUM: ' + str(ConfigManager.getConfig('ACTIVATED_TEST_PACK_NUM')))
            self.skipOnlineSyncsDueToTestConfig = True

        URLs = generateURLs()
        self.mainPageURL = URLs['mainPageURL']
        self.allServicesURL = URLs['allServicesURL']

        TRACE('DATA_COLLECTOR_CONFIGURED')
    
    def keepCollectingData(self):
        returnMessage = { 'success': False,
                          'error': False,
                          'finished': False,
                          'message': ''}
        try:
            if self.phase == cp.GITHUB_SYNCHRONIZATION:
                TRACE('[CP] GITHUB_SYNCHRONIZATION')
                if (not self.skipOnlineSyncsDueToTestConfig):
                    githubSynchronization()
                    TRACE('CENTRAL_DATA_GATHERED')
                else:
                    TRACE('TEST_PACK_NUM_ACTIVATED - skipping gathering central data')

            elif self.phase == cp.CONFIGURE_DAYS_AND_WEEK_SCHEDULE:
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
                    self.phase = cp.END
                else:
                    TRACE('PERFORMING_UPDATE')

            #########################################################################
            #########################################################################
            #########################################################################

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
                result = deleteNecessaryData()
                self.canUseOldWorkDayResources = result['canUseOldWorkDayResources']
                self.canUseOldSaturdayResources = result['canUseOldSaturdayResources']
                self.canUseOldSundayResources = result['canUseOldSundayResources']
                TRACE('Old Work Day resources enabled: ' + str(self.canUseOldWorkDayResources))
                TRACE('Old Saturday resources enabled: ' + str(self.canUseOldSaturdayResources))
                TRACE('Old Sunday resources enabled: ' + str(self.canUseOldSundayResources))
                
            elif self.phase == cp.EXTRACT_RULES:
                TRACE('[CP] EXTRACT_RULES')
                self.fileNames = extractRules(self.workDayLinks,
                                              self.saturdayLinks,
                                              self.sundayLinks,
                                              self.specialDayLinks,
                                              self.weekSchedule,
                                              self.mondayDate,
                                              self.canUseOldWorkDayResources,
                                              self.canUseOldSaturdayResources,
                                              self.canUseOldSundayResources)
                
            elif self.phase == cp.ADD_DECRYPTED_SERVICES:
                TRACE('[CP] ADD_DECRYPTED_SERVICES')
                result = addDecryptedServices(self.days,
                                              self.weekSchedule,
                                              self.mondayDate,
                                              self.fileNames)
                self.missingServices = result['missingServices']
                
            elif self.phase == cp.ADD_DECRYPTED_SHIFTS:
                TRACE('[CP] ADD_DECRYPTED_SHIFTS')
                addDecryptedShifts(self.days,
                                   self.weekSchedule,
                                   self.mondayDate,
                                   self.fileNames)

            elif self.phase == cp.CONFIGURE_NOTIFICATION_FILES:
                TRACE('[CP] CONFIGURE_NOTIFICATION_FILES')
                configureNotificationsFiles(self.notificationsLinks)

            elif self.phase == cp.SET_NEW_WARNINGS:
                TRACE('[CP] SET_NEW_WARNINGS')
                WarningMessagesManager.setWarningMessages()

            elif self.phase == cp.PUSH_NEW_UPDATE_INFO:
                TRACE('[CP] PUSH_NEW_UPDATE_INFO')
                mondayDateList = [self.mondayDate.year,
                                  self.mondayDate.month,
                                  self.mondayDate.day]
                UpdateInfoManager.pushNewUpdateInfo(mondayDateList, self.servicesHash, self.missingServices)
                UpdateInfoManager.setDataUpdated()

            elif self.phase == cp.UPLOAD_DATA:
                TRACE('[CP] UPLOAD_DATA')
                if (not self.skipOnlineSyncsDueToTestConfig):
                    uploadData()
                    TRACE('DATA_UPLOADED_SUCCESSFULLY')
                else:
                    TRACE('TEST_PACK_NUM_ACTIVATED - skipping uploading central data')

            #########################################################################
            #########################################################################
            #########################################################################

            if (self.phase != cp.END):
                self.phase = cp(self.phase.value + 1)
                returnMessage['message'] = COLLECT_PHASE_OUTPUT_MESSAGE_MAP[self.phase]

            if (self.phase == cp.END):
                returnMessage['finished'] = True
                returnMessage['success'] = UpdateInfoManager.isDataUpdated()
                ConfigManager.completeDataRecovery()
                
        except Exception as e:
            TRACE(e)

            return {'success': False,
                    'error': True,
                    'finished': True,
                    'message': 'GRESKA! Popravljanje dokumenata'}

        return returnMessage
