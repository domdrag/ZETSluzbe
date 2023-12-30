import json

def getNotifications():
    with open('data/central_data/notifications.json', 'r', encoding = 'utf-8') as notificationsFile:
        NOTIFICATIONS = json.load(notificationsFile)

    return NOTIFICATIONS

def setNotifications(NOTIFICATIONS):
    with open('data/central_data/notifications.json', 'w', encoding = 'utf-8') as notificationsFile:
        json.dump(NOTIFICATIONS, notificationsFile, indent = 3)