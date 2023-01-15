import os

def deleteExceeded(directory):
    files = os.listdir('data/' + directory)
    if(directory == 'all_services_by_driver_decrypted'):
        maxExceed = 7
    else:
        maxExceed = 21

    for file in files:
        if(file == 'keep.txt'): # gitHub ne dozvoljava prazan folder
            continue
        fileName = 'data/' + directory + '/' + file
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
        
def deleteNecessaryFiles():
    files = os.listdir('data')
    for file in files:
        # overkilling with conditions
        if file == 'all_drivers.txt':
            continue
        elif file == 'tram.png':
            continue
        elif 'copy' in file:
            continue
        elif 'last_record_date.txt' in file:
            continue
        elif 'warnings.txt' in file:
            continue
        elif 'all_services_by_driver_decrypted' in file:
            continue
        elif 'all_shifts_by_driver_decrypted' in file:
            continue
        else:
            os.remove('data/' + file)

    deleteExceeded('all_services_by_driver_decrypted')
    deleteExceeded('all_shifts_by_driver_decrypted')
