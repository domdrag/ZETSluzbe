from kivymd.color_definitions import colors

LIGHT_HUE = '200'
MAIN_HUE = '500'
DARK_HUE = '700'
PRIMARY_COLOR = 'Blue'
SECONDARY_COLOR = 'Amber'
SERVICE_COLOR = 'BlueGray'
SHIFT_COLOR = 'BlueGray'
FREE_DAY_COLOR = 'Green'
ERROR_COLOR = 'Red'

def getColors():
    return colors

def getPrimaryColor():
    return colors[PRIMARY_COLOR][DARK_HUE]

def getPrimaryColorString():
    return PRIMARY_COLOR

def getSecondaryColor():
    return colors[SECONDARY_COLOR][DARK_HUE]

def getSecondaryColorString():
    return SECONDARY_COLOR

def getServiceColor():
    return colors[SERVICE_COLOR][DARK_HUE]

def getShiftColor():
    return colors[SHIFT_COLOR][DARK_HUE]

def getFreeDayColor():
    return colors[FREE_DAY_COLOR][MAIN_HUE]

def getErrorColor():
    return colors[ERROR_COLOR][DARK_HUE]

def getWhiteColor():
    return (1, 1, 1, 1)


