import json

from src.share.filenames import NOTIFICATIONS_PATH

def getNotifications():
    with open(NOTIFICATIONS_PATH, 'r', encoding = 'utf-8') as notificationsFile:
        NOTIFICATIONS = json.load(notificationsFile)

    return NOTIFICATIONS

def setNotifications(NOTIFICATIONS):
    with open(NOTIFICATIONS_PATH, 'w', encoding = 'utf-8') as notificationsFile:
        json.dump(NOTIFICATIONS, notificationsFile, indent = 3)