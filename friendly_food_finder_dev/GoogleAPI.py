from __future__ import print_function

from datetime import datetime, timedelta
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_scheudle(hours=2):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        print(datetime.utcnow())
        now = datetime.utcnow()
        events_result = service.events().list(calendarId='primary', timeMin=dateTimeToString(now),
                                              timeMax=dateTimeToString(now + timedelta(hours=2)), singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            if event["start"].get("dateTime"):
                start = event["start"].get("dateTime")[:-3] + event["start"].get("dateTime")[-2:]
                print(datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z'))
            print(event['summary'], "lol", event["start"].get("dateTime"), "heehee", event["end"].get("dateTime"))

    except HttpError as error:
        print('An error occurred: %s' % error)

def stringToDateTime(str):
    if str != None:
        str = str["start"].get("dateTime")[:-3] + str["start"].get("dateTime")[-2:]
        return datetime.datetime.strptime(str, '%Y-%m-%dT%H:%M:%S%z')
    else:
        return None
    
def dateTimeToString(time):
    return time.isoformat() + 'Z'