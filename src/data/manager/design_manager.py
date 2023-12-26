import json

DESIGN_FILE_PATH = 'data/design.json'

class DesignManager:
    __colorsImpl__ = dict()
    __design__ = dict()
    __customColors__ = dict()

    @staticmethod
    def load():
        with open(DESIGN_FILE_PATH, 'r') as designFile:
            DesignManager.__design__ = json.load(designFile)
        DesignManager.__customColors__ = DesignManager.__design__['CUSTOM_COLORS']

        # import problematic for kivy loggings in env. setup (needs to be postponed)
        import kivymd.color_definitions as kivyColors
        DesignManager.__colorsImpl__ = kivyColors.colors

    @staticmethod
    def getLoginScreenFontSize():
        return DesignManager.__design__['LOGIN_SCREEN_FONT_SIZE']

    @staticmethod
    def getMainScreenFontSize():
        return DesignManager.__design__['MAIN_SCREEN_FONT_SIZE']

    @staticmethod
    def getLogsFontSize():
        return DesignManager.__design__['LOGS_FONT_SIZE']

    @staticmethod
    def getGridHeight():
        return DesignManager.__design__['MAIN_GRID_HEIGHT']

    @staticmethod
    def updateFontSize(screen, value):
        DesignManager.__design__[screen] = str(value) + 'dp'
        with open(DESIGN_FILE_PATH, 'w') as designFile:
            json.dump(DesignManager.__design__, designFile, indent=3)

    @staticmethod
    def updateGridHeight(value):
        DesignManager.__design__['MAIN_GRID_HEIGHT'] = str(value) + 'dp'
        with open(DESIGN_FILE_PATH, 'w') as designFile:
            json.dump(DesignManager.__design__, designFile, indent=3)

    @staticmethod
    def getColors():
        return DesignManager.__colorsImpl__

    @staticmethod
    def getPrimaryColor():
        colorsImpl = DesignManager.__colorsImpl__
        customColors = DesignManager.__customColors__
        return colorsImpl[customColors['PRIMARY_COLOR']][customColors['DARK_HUE']]

    @staticmethod
    def getPrimaryColorLight():
        colorsImpl = DesignManager.__colorsImpl__
        customColors = DesignManager.__customColors__
        return colorsImpl[customColors['PRIMARY_COLOR']][customColors['MAIN_HUE']]

    @staticmethod
    def getPrimaryColorString():
        return DesignManager.__customColors__['PRIMARY_COLOR']

    @staticmethod
    def getSecondaryColor():
        colorsImpl = DesignManager.__colorsImpl__
        customColors = DesignManager.__customColors__
        return colorsImpl[customColors['SECONDARY_COLOR']][customColors['DARK_HUE']]

    @staticmethod
    def getSecondaryColorString():
        return DesignManager.__customColors__['SECONDARY_COLOR']

    @staticmethod
    def getServiceColor():
        colorsImpl = DesignManager.__colorsImpl__
        customColors = DesignManager.__customColors__
        return colorsImpl[customColors['SERVICE_COLOR']][customColors['DARK_HUE']]

    @staticmethod
    def getShiftColor():
        colorsImpl = DesignManager.__colorsImpl__
        customColors = DesignManager.__customColors__
        return colorsImpl[customColors['SHIFT_COLOR']][customColors['DARK_HUE']]

    @staticmethod
    def getFreeDayColor():
        colorsImpl = DesignManager.__colorsImpl__
        customColors = DesignManager.__customColors__
        return colorsImpl[customColors['FREE_DAY_COLOR']][customColors['MAIN_HUE']]

    @staticmethod
    def getErrorColor():
        colorsImpl = DesignManager.__colorsImpl__
        customColors = DesignManager.__customColors__
        return colorsImpl[customColors['ERROR_COLOR']][customColors['DARK_HUE']]

    @staticmethod
    def getWhiteColor():
        return (1, 1, 1, 1)


