import json

def getNotifications():
    with open('data/data/notifications.json', 'r', encoding='utf-8') as notificationsFile:
        NOTIFICATIONS = json.load(notificationsFile)

    return NOTIFICATIONS

def readNotifications():
    notifications = getNotifications()
    notificationsData = []

    for notificationText, notificationLink in notifications.items():
        notificationsData.append({'notificationText': notificationText,
                                  'notificationLink': notificationLink['URL']})
    return notificationsData

