
def getWarningMessageInfo():
    fileR = open('data/data/warnings.txt', 'r', encoding='utf-8')
    message = fileR.read()
    fileR.close()

    if (message == ''):
        return {'message': '[ERROR] Warning message ne postoji.'}

    return {'message': message}

