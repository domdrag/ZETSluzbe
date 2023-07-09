import json

def getDesignJSON():
    with open('data/design.json', 'r') as designFile:
        design = json.load(designFile)

    return design

def getDesign(designScreen):
    with open('data/design.json', 'r') as designFile:
        design = json.load(designFile)

    return design[designScreen]

def setDesign(designScreen, designName, designValue):
    design = getDesign(designScreen)

    design[designName] = designValue
    
    with open('data/design.json', 'w') as designFile:
        json.dump(design, designFile, indent = 3)

def updateFontSize(screen, isIncrease):
    designJSON = getDesignJSON()
    design = designJSON[screen]

    fontSize = design['FONT_SIZE']
    if (fontSize[:2].isdigit()):
        size = int(fontSize[:2])
    else:
        size = int(fontSize[0])

    if (isIncrease):
        size = size + 1
    else:
        size = size - 1
    design['FONT_SIZE'] = str(size) + 'dp'

    designJSON[screen] = design

    with open('data/design.json', 'w') as designFile:
        json.dump(designJSON, designFile, indent = 3)
