from src.data.share.color_manager import getWhiteColor, getErrorColor

def readWarningMessage():
    fileR = open('data/data/warnings.txt', 'r', encoding='utf-8')
    lines = fileR.readlines()
    fileR.close()
    return lines

def getWarningMessageInfo():
    lines = readWarningMessage()
    if (lines == []):
        return {'message': '[ERROR] Warning message ne postoji.',
                'color': getErrorColor()}
        
    firstMessage = lines[0].split('$')
    message = firstMessage[1]
    if (firstMessage[0] == '0'):
        color = getWhiteColor()
    elif (firstMessage[0] == '1'):
        color = getWhiteColor()
    else:
        color = getErrorColor()

    for line in lines[1:]:
        message += line

    assert isinstance(message, str)
    return {'message': message, 'color': color}

