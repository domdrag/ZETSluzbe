
def addWarningMessage(message):
    fileA = open('data/data/warnings.txt', 'a', encoding='utf-8')
    fileA.write(message)
    fileA.close()