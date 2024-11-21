from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def create_event(task):
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = Credentials.from_authorized_user_file('credentials.json', SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    event = {
        'summary': task.title,
        'description': task.description,
        'start': {'dateTime': task.deadline.isoformat(), 'timeZone': 'UTC'},
        'end': {'dateTime': (task.deadline + timedelta(hours=1)).isoformat(), 'timeZone': 'UTC'},
    }
    event_result = service.events().insert(calendarId='primary', body=event).execute()
    return event_result
