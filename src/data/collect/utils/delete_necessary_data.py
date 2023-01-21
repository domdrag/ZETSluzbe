import os

def deleteExceeded(directory):
    files = os.listdir('data/data/' + directory)
    if(directory == 'all_services_by_driver_decrypted'):
        maxExceed = 7
    else:
        maxExceed = 21

    for file in files:
        if(file == '000keep.txt'): # gitHub ne dozvoljava prazan folder
            continue
        fileName = 'data/data/' + directory + '/' + file
        fileR = open(fileName, 'r', encoding='utf-8')
        lines = fileR.readlines()
        fileR.close()

        if(len(lines) <= maxExceed):
            return

        fileW = open(fileName, 'w', encoding='utf-8')
        for i in range(len(lines)):
            if(len(lines) - i > maxExceed):
                pass
            else:
                fileW.write(lines[i])
        fileW.close()
        
def deleteNecessaryData():
    files = os.listdir('data/data')
    for file in files:
        ##if False:
        ##    pass
        ###### NEEDED DATA DURING UPDATING ############
        ##if 'last_record_date.txt' in file:
        ##    continue
        ##elif 'warnings.txt' in file:
        ##    continue
        if 'tpd.pdf' in file: # needed for extractRulesByDriver()
            continue
        elif 'all_drivers.txt' in file: # needed for writeDecryptedShifts()
            continue
        ###### NEEDED DATA FOR APPENDING ############
        elif 'all_services_by_driver_decrypted' in file: 
            continue
        elif 'all_shifts_by_driver_decrypted' in file:
            continue
        #############################################
        else:
            os.remove('data/data/' + file)

    deleteExceeded('all_services_by_driver_decrypted')
    deleteExceeded('all_shifts_by_driver_decrypted')
