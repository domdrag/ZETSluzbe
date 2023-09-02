import json

from kivymd.color_definitions import colors as kivyColors

DESIGN_FILE_PATH = 'data/design.json'
COLORS_IMPL = kivyColors
DESIGN = dict()
CUSTOM_COLORS = dict()

def loadDesign():
    global DESIGN
    global CUSTOM_COLORS

    with open(DESIGN_FILE_PATH, 'r') as designFile:
        DESIGN = json.load(designFile)
    CUSTOM_COLORS = DESIGN['CUSTOM_COLORS']

def getFontSize():
    return DESIGN['FONT_SIZE']

def getLoginScreenFontSize():
    return DESIGN['LOGIN_SCREEN_FONT_SIZE']

def getMainScreenFontSize():
    return DESIGN['MAIN_SCREEN_FONT_SIZE']

def getGridHeight():
    return DESIGN['MAIN_GRID_HEIGHT']

def updateFontSize(screen, value):
    DESIGN[screen] = str(value) + 'dp'
    with open(DESIGN_FILE_PATH, 'w') as designFile:
        json.dump(DESIGN, designFile, indent = 3)

def updateGridHeight(value):
    DESIGN['MAIN_GRID_HEIGHT'] = str(value) + 'dp'
    with open(DESIGN_FILE_PATH, 'w') as designFile:
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

