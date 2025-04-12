import os
import pickle
import datetime
import parsedatetime as pdt
import re
import pytz
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('oauth_credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)
    return build('calendar', 'v3', credentials=creds)

def parse_datetime(natural_datetime):
    cal = pdt.Calendar()
    time_struct, parse_status = cal.parse(natural_datetime)

    if not time_struct or time_struct.tm_year == 1900:
        raise ValueError(f"Could not parse datetime: '{natural_datetime}'")

    dt = datetime.datetime(*time_struct[:6])

    # If no time was provided, default to 10 AM
    if (time_struct.tm_hour == 0 and time_struct.tm_min == 0) and (
        'at' not in natural_datetime.lower()
    ):
        dt = dt.replace(hour=10, minute=0)

    # Localize to Asia/Kolkata
    india_tz = pytz.timezone('Asia/Kolkata')
    localized_dt = india_tz.localize(dt)

    return localized_dt

def extract_email(email_string):
    match = re.search(r'[\w\.-]+@[\w\.-]+', email_string)
    return match.group() if match else None

def create_event(details, include_meet=True):
    if 'date_time' not in details:
        raise ValueError("Missing 'date_time' in details")

    start_time = parse_datetime(details['date_time'])
    end_time = start_time + datetime.timedelta(hours=1)

    attendees = []
    for attendee in details.get('attendees', []):
        email = extract_email(attendee)
        if email:
            attendees.append({'email': email})

    if not attendees:
        raise ValueError("No valid attendee emails found.")

    event = {
        'summary': details['purpose'],
        'description': f"{details['description']}\nPlatform: {details['platform']}",
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'attendees': attendees
    }

    if include_meet:
        event['conferenceData'] = {
            'createRequest': {
                'requestId': f"smart-scheduler-{int(datetime.datetime.now().timestamp())}",
                'conferenceSolutionKey': {'type': 'hangoutsMeet'}
            }
        }

    service = get_calendar_service()

    created_event = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1,
        sendUpdates='all'
    ).execute()

    return created_event.get('htmlLink')

def find_event_by_email_and_purpose(attendee_email, purpose_keyword):
    service = get_calendar_service()
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        maxResults=100,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    for event in events_result.get('items', []):
        if purpose_keyword.lower() in event.get('summary', '').lower():
            for a in event.get('attendees', []):
                if a.get('email') == attendee_email:
                    return event

    return None

def reschedule_event_by_email_and_purpose(attendee_email, purpose_keyword, new_datetime):
    service = get_calendar_service()

    old_event = find_event_by_email_and_purpose(attendee_email, purpose_keyword)
    if not old_event:
        raise ValueError("No matching event found for the given attendee and purpose.")

    new_start = parse_datetime(new_datetime)
    new_end = new_start + datetime.timedelta(hours=1)

    event_id = old_event['id']

    updated_event = {
        'summary': old_event['summary'],
        'description': old_event.get('description', ''),
        'start': {'dateTime': new_start.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': new_end.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'attendees': old_event.get('attendees', []),
        'conferenceData': old_event.get('conferenceData', {})
    }

    updated = service.events().update(
        calendarId='primary',
        eventId=event_id,
        body=updated_event,
        sendUpdates='all',
        conferenceDataVersion=1
    ).execute()

    return updated.get('htmlLink')

def delete_event(event_id):
    try:
        service = get_calendar_service()
        service.events().delete(
            calendarId='primary',
            eventId=event_id,
            sendUpdates='all'
        ).execute()
        print(f"Deleted event: {event_id}")
    except Exception as e:
        print(f"Failed to delete event: {e}")

def force_reschedule_by_email_and_purpose(attendee_email, purpose_keyword, new_datetime):
    service = get_calendar_service()

    old_event = find_event_by_email_and_purpose(attendee_email, purpose_keyword)
    if not old_event:
        raise ValueError("No matching event found.")

    try:
        delete_event(old_event['id'])
    except Exception as e:
        print(f"Couldn't delete old event: {e}")

    description_lines = old_event.get('description', '').split('\n')
    details = {
        'purpose': old_event['summary'],
        'description': description_lines[0] if description_lines else "",
        'platform': "Google Meet",
        'date_time': new_datetime,
        'attendees': [a['email'] for a in old_event.get('attendees', [])]
    }

    link = create_event(details)
    print(f"Rescheduled event link: {link}")
    return link

def get_task_reminder_events():
    service = get_calendar_service()
    now = datetime.datetime.utcnow().isoformat() + 'Z'

    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        maxResults=20,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    task_reminders = []
    for event in events:
        summary = event.get("summary", "")
        if summary.startswith("Reminder:"):
            title = summary.replace("Reminder:", "").strip()
            start_time = event['start'].get('dateTime', event['start'].get('date'))
            task_reminders.append((title, start_time))

    return task_reminders
