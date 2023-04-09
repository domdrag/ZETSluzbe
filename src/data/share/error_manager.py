
def errorOccuredInLastSession():
    fileR = open('data/data/update_successful.txt', 'r', encoding='utf-8')
    line = fileR.read()
    fileR.close()
    
    if line == '1':
        return False
    return True

# bad programming but left for code clarity
def unsetUpdateSuccessful():
    fileW = open('data/data/update_successful.txt', 'w', encoding='utf-8')
    fileW.write('0')
    fileW.close()

def setUpdateSuccessful():
    fileW = open('data/data/update_successful.txt', 'w', encoding='utf-8')
    fileW.write('1')
    fileW.close()

