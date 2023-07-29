import json

from kivymd.color_definitions import colors as kivyColors

COLORS_IMPL = kivyColors
DESIGN = dict()
CUSTOM_COLORS = dict()
def loadDesign():
    global DESIGN
    global CUSTOM_COLORS

    with open('data/design.json', 'r') as designFile:
        DESIGN = json.load(designFile)
    CUSTOM_COLORS = DESIGN['CUSTOM_COLORS']

def getFontSize():
    return DESIGN['FONT_SIZE']
def updateFontSize(value):
    DESIGN['FONT_SIZE'] = str(value) + 'dp'
    with open('data/design.json', 'w') as designFile:
        json.dump(DESIGN, designFile, indent = 3)

def getColors():
    return COLORS_IMPL

def getPrimaryColor():
    return COLORS_IMPL[CUSTOM_COLORS['PRIMARY_COLOR']][CUSTOM_COLORS['DARK_HUE']]

def getPrimaryColorString():
    return CUSTOM_COLORS['PRIMARY_COLOR']

def getSecondaryColor():
    return COLORS_IMPL[CUSTOM_COLORS['SECONDARY_COLOR']][CUSTOM_COLORS['DARK_HUE']]

def getSecondaryColorString():
    return CUSTOM_COLORS['SECONDARY_COLOR']

def getServiceColor():
    return COLORS_IMPL[CUSTOM_COLORS['SERVICE_COLOR']][CUSTOM_COLORS['DARK_HUE']]

def getShiftColor():
    return COLORS_IMPL[CUSTOM_COLORS['SHIFT_COLOR']][CUSTOM_COLORS['DARK_HUE']]

def getFreeDayColor():
    return COLORS_IMPL[CUSTOM_COLORS['FREE_DAY_COLOR']][CUSTOM_COLORS['MAIN_HUE']]

def getErrorColor():
    return COLORS_IMPL[CUSTOM_COLORS['ERROR_COLOR']][CUSTOM_COLORS['DARK_HUE']]

def getWhiteColor():
    return (1, 1, 1, 1)

