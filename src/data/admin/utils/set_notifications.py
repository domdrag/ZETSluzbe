import json
import os
import shutil

from src.data.share.generate_notification_files import generateNotificationFiles

GENERATED_IMAGE_RESOLUTION = 300
NOTIFICATIONS_FILES_PATH = 'data/data/notificationsFiles/'

def clearNotificationsFilesDir():
    if (os.path.isdir(NOTIFICATIONS_FILES_PATH)):
        shutil.rmtree(NOTIFICATIONS_FILES_PATH)
    os.mkdir(NOTIFICATIONS_FILES_PATH)

def setNotifications(notifications):
    NOTIFICATIONS = dict()

    clearNotificationsFilesDir()
    for notification in notifications:
        NOTIFICATIONS[notification['name']] = {'URL': notification['URL']}
        generateNotificationFiles(notification['name'], notification['URL'])

    with open('data/data/notifications.json', 'w', encoding='utf-8') as notificationsFile:
        json.dump(NOTIFICATIONS, notificationsFile, indent = 3)