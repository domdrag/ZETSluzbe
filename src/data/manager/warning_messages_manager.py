from src.share.filenames import WARNINGS_PATH

class WarningMessagesManager:
    __updatedWarningMessages__ = []

    @staticmethod
    def load():
        WarningMessagesManager.__updatedWarningMessages__ = []

    @staticmethod
    def addWarningMessage(warningMessage):
        WarningMessagesManager.__updatedWarningMessages__.append(warningMessage + '\n')

    @staticmethod
    def setWarningMessages():
        fileW = open(WARNINGS_PATH, 'w', encoding='utf-8')
        for warningMessage in WarningMessagesManager.__updatedWarningMessages__:
            fileW.write(warningMessage)
        fileW.close()