from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
# Authenticate using the service account
credentials = Credentials.from_authorized_user_file(os.getenv('AUTH_FILE_PATH'), scopes=os.getenv('SCOPES'))
service = build('calendar', 'v3', credentials=credentials)

def create_gcal_event(event_name, description, start_time, end_time):
    """Creates an event on the specified Google Calendar."""
    event = {
        'summary': event_name,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/Denver',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/Denver',
        },
    }

    # Add the event to the calendar
    event = service.events().insert(calendarId=os.getenv('CALENDAR_ID'), body=event).execute()
    print(f"Event created: {event.get('htmlLink')}")

# Example usage
if __name__ == "__main__":

    create_gcal_event(
        event_name="Test",
        description="Discussion of project updates.",
        start_time= "2025-1-13T12:00:00",
        end_time="2025-1-13T12:30:00",
    )
