
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
        fileW = open('data/central_data/warnings.txt', 'w', encoding='utf-8')
        for warningMessage in WarningMessagesManager.__updatedWarningMessages__:
            fileW.write(warningMessage)
        fileW.close()