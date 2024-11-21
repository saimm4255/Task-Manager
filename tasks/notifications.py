import firebase_admin
from firebase_admin import messaging, credentials

cred = credentials.Certificate('path/to/firebase_credentials.json')
firebase_admin.initialize_app(cred)

def send_notification(user, message):
    token = user.profile.fcm_token  
    notification = messaging.Notification(
        title="Task Update",
        body=message,
    )
    message = messaging.Message(notification=notification, token=token)
    response = messaging.send(message)
    return response
