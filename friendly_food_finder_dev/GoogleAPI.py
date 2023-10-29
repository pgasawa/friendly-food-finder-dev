from __future__ import print_function

from datetime import datetime, timedelta
import os.path
import json
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from friendly_food_finder_dev.firebase import firestore_client

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_user_token():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return creds.to_json()

def does_user_have_conflict(user_doc, startHourInterval=0, endHourInterval=2):
    """Finds if there are any conflicting events in the next hours.
    Looks for events anywhere between now+startHourInterval and now+endHourInterval.
    Returns True if there is any events within the next hours.
    Returns False if there are no events in the next hours.
    NOTE: Full day events are also considered conflicts.
    """
    try:
        creds = Credentials.from_authorized_user_info(json.loads(user_doc['token']), SCOPES)

        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.utcnow()
        events_result = service.events().list(calendarId='primary', timeMin=dateTimeToString(now + timedelta(hours=startHourInterval)),
                                              timeMax=dateTimeToString(now + timedelta(hours=endHourInterval)), singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        
        noFullDayEvents = []
        for event in events:
            if event["start"].get("dateTime") != None:
                noFullDayEvents.append(event)
        events = noFullDayEvents

        if not events:
            print('No upcoming events found.')
            return False

        for event in events:
            print(event['summary'], "|", event["start"], "|", event["end"])
        return True

    except HttpError as error:
        print('An error occurred: %s' % error)
        return True

def send_cal_invite(organizerEmail: str, attendeeEmails: List[str], startTime: str, location: str):
    user_doc = firestore_client.read_from_document('user', organizerEmail)
    creds = Credentials.from_authorized_user_info(json.loads(user_doc['token']), SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    event = {
        'summary': 'Lunch! ',
        'location': location,
        'description': 'Time to eat.',
        'start': {
            'dateTime': startTime,
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': startTime + timedelta(hours=1),
            'timeZone': 'America/Los_Angeles',
        },
        'attendees': [
            {'email': attendeeEmail} for attendeeEmail in attendeeEmails
        ],
    }
    event = service.events().insert(calendarId='primary', body=event).execute()

def stringToDateTime(str):
    if str != None:
        str = str["start"].get("dateTime")[:-3] + str["start"].get("dateTime")[-2:]
        return datetime.datetime.strptime(str, '%Y-%m-%dT%H:%M:%S%z')
    else:
        return None
    
def dateTimeToString(time):
    return time.isoformat() + 'Z'