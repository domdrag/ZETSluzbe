import os

def deleteNecessaryData():
    files = os.listdir('data/data')
    for file in files:
        # need to delete these files so we don't end up with garbage files
        # should be equivalent to the older function
        if 'rules' in file:
            os.remove('data/data/' + file)

'''
def deleteNecessaryData():
    files = os.listdir('data/data')
    for file in files:
        ###### NEEDED DATA DURING UPDATING ############
        if 'tpd.pdf' in file: # needed for extractRulesByDriver()
            continue
        elif 'all_drivers.txt' in file: # needed for writeDecryptedShifts()
            continue
        elif 'tram' in file: # needed for buildozer [not needed for updating]
            continue
        ###### NEEDED DATA FOR APPENDING ############
        elif 'all_services_by_driver_decrypted' in file: 
            continue
        elif 'all_shifts_by_driver_decrypted' in file:
            continue
        elif 'holidays' in file:
            continue
        elif 'statistics' in file:
            continue
        elif 'week' in file:
            continue
        elif 'warning' in file:
            continue
        elif 'notifications' in file:
            continue
        #############################################
        else:
            os.remove('data/data/' + file)
'''