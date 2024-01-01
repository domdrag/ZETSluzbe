from src.share.filenames import WARNINGS_PATH

def getWarningMessageInfo():
    fileR = open(WARNINGS_PATH, 'r', encoding='utf-8')
    message = fileR.read()
    fileR.close()

    if (message == ''):
        return {'message': '[ERROR] Warning message ne postoji.'}

    return {'message': message}

