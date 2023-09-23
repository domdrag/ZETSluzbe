from src.data.manager.notifications_manager import getNotifications

def readNotifications():
    notifications = getNotifications()
    notificationsData = []

    for notificationText, notificationLink in notifications.items():
        notificationsData.append({'notificationText': notificationText,
                                  'notificationLink': notificationLink['URL']})
    return notificationsData

