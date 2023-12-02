
class WarningMessagesManager:
    warningMessages = []

    @staticmethod
    def addWarningMessage(warningMessage):
        WarningMessagesManager.warningMessages.append(warningMessage)

    @staticmethod
    def clearWarningMessages():
        WarningMessagesManager.warningMessages = []

    @staticmethod
    def setWarningMessages():
        fileW = open('data/data/warnings.txt', 'w', encoding='utf-8')
        for warningMessage in WarningMessagesManager.warningMessages:
            fileW.write(warningMessage)
        fileW.close()
        WarningMessagesManager.clearWarningMessages()