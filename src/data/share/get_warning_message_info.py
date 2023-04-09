
COLOR_TUPLE_SIZE = 4

def readWarningMessage():
    fileR = open('data/data/warnings.txt', 'r', encoding='utf-8')
    lines = fileR.readlines()
    fileR.close()
    return lines

def getWarningMessageInfo():
    lines = readWarningMessage()
    if(lines == []):
        return
        
    firstMessage = lines[0].split('$')
    message = firstMessage[1]
    if(firstMessage[0] == '0'):
        color = (0.2,0.71,0.13,1)
    else:
        color = (0.96,0.74,0,1)

    for line in lines[1:]:
        message += line

    assert isinstance(message, str)
    assert isinstance(color, tuple)
    assert len(color) == COLOR_TUPLE_SIZE
    return {'message': message, 'color': color}

