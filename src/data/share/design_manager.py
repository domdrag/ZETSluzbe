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

def updateFontSize(screen, value):
    designJSON = getDesignJSON()
    design = designJSON[screen]    
    design['FONT_SIZE'] = str(value) + 'dp'
    designJSON[screen] = design

    with open('data/design.json', 'w') as designFile:
        json.dump(designJSON, designFile, indent = 3)
