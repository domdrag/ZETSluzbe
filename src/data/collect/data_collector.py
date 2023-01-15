from datetime import date

from src.data.collect.utils.collect_phase import CollectPhase

from src.data.collect.services_decrypted.write_decrypted_services import (
    writeDecryptedServices
    )
from src.data.collect.shifts_decrypted.write_decrypted_shifts import (
    writeDecryptedShifts
    )
from src.data.collect.utils.delete_necessary_files import deleteNecessaryFiles 
from src.data.collect.utils.search_links import searchLinks  
from src.data.collect.utils.set_last_record import setLastRecord   
from src.data.collect.utils.set_days import setDays
from src.data.collect.rules.extract_rules_by_driver import extractRulesByDriver
from src.data.collect.rules.extract_rules import extractRules

cp = CollectPhase

class DataCollector:
    phase = cp.SEARCH_LINKS
    days = []
    workDayURL = ''
    saturdayURL = ''
    sundayURL = ''
    mondayDate = date(2022,1,1)
    weekSchedule = ['W','W','W','W','W','W','W']
    
    def keepCollectingData(self):
        returnMessage = { 'success': False,
                          'error': False,
                          'finished': False,
                          'message': '' }
        try:
            match self.phase:
                case cp.SEARCH_LINKS:
                    #print('SEARCH_LINKS')
                    foundLinks = searchLinks()
                    self.workDayURL = foundLinks['workDay']
                    self.saturdayURL = foundLinks['saturday']
                    self.sundayURL = foundLinks['sunday']
                    returnMessage['message'] = 'Brisanje potrebnih dokumenata'
                case cp.DELETE_NECESSARY_FILES:
                    #print('DELETE_NECESSARY_FILES')
                    deleteNecessaryFiles()
                    returnMessage['message'] = 'Postavljanje datuma'
                case cp.SET_DAYS:
                    #print('SET_DAYS')
                    result = setDays(self.days)
                    updateNeeded = result['updateNeeded']
                    if(updateNeeded == False):
                        returnMessage['finished'] = True
                        returnMessage['message'] = 'Sluzbe jos nisu izasle!'
                    else:
                        self.mondayDate = result['mondayDate']
                        returnMessage['message'] = \
                                     'Citanje tjednih sluzbi'
                case cp.EXTRACT_RULES_BY_DRIVER:
                    #print('EXTRACT_RULES_BY_DRIVER')
                    extractRulesByDriver(self.weekSchedule)
                    returnMessage['message'] = 'Citanje svih sluzbi'
                case cp.EXTRACT_RULES:
                    #print('EXTRACT_RULES')
                    extractRules(self.workDayURL,
                                 self.saturdayURL,
                                 self.sundayURL)
                    returnMessage['message'] = 'Zapisivanje tjednih sluzbi'
                case cp.WRITE_DECRYPTED_SERVICES:
                    #print('WRITE_DECRYPTED_SERVICES')
                    writeDecryptedServices(self.days, self.weekSchedule)
                    returnMessage['message'] = 'Zapisivanje tjednih smjena'
                case cp.WRITE_DECRYPTED_SHIFTS:
                    #print('WRITE_DECRYPTED_SHIFTS')
                    writeDecryptedShifts(self.days, self.weekSchedule)
                    returnMessage['message'] = \
                                 'Postavljanje datuma zadnjeg azuriranja'
                case cp.SET_LAST_RECORD:
                    #print('SET_LAST_RECORD')
                    setLastRecord(self.mondayDate)
                    returnMessage['success'] = True
                    returnMessage['finished'] = True
                    returnMessage['message'] = 'Kopiranje sluzbi'
                
        except Exception as e:
            #print(e)
            return {'success': False,
                    'error': True,
                    'finished': True,
                    'message': 'GRESKA! Popravljanje dokumenata'}
        self.phase = cp(self.phase.value + 1)
        if self.phase == cp.END:
            self.phase = cp.SEARCH_LINKS
        return returnMessage

