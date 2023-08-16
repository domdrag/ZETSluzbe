import json

NOTIFICATIONS = dict()
def setNotifications(notifications):
    for notification in notifications:
        NOTIFICATIONS[notification['name']] = {'URL': notification['URL']}

    with open('data/data/notifications.json', 'w', encoding='utf-8') as notificationsFile:
        json.dump(NOTIFICATIONS, notificationsFile, indent = 3)