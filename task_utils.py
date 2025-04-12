# task_utils.py
import datetime
import parsedatetime as pdt
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import pickle
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/tasks']
DEFAULT_ATTENDEE = os.getenv("EMAIL_ADDRESS")

def get_tasks_service():
    creds = None
    if os.path.exists('token_tasks.pkl'):
        with open('token_tasks.pkl', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('oauth_credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token_tasks.pkl', 'wb') as token:
            pickle.dump(creds, token)
    return build('tasks', 'v1', credentials=creds)

def parse_datetime(natural_datetime):
    cal = pdt.Calendar()
    time_struct, _ = cal.parse(natural_datetime)
    dt = datetime.datetime(*time_struct[:6])
    
    # Default time if none is provided
    if time_struct.tm_hour == 0 and time_struct.tm_min == 0 and 'at' not in natural_datetime.lower():
        dt = dt.replace(hour=10, minute=0)
    
    return dt


def create_google_task(title, due_date):
    service = get_tasks_service()
    task_time = parse_datetime(due_date)
    iso_due = task_time.isoformat() + 'Z'

    task = {
        'title': title,
        'due': iso_due,
        'status': 'needsAction'
    }

    result = service.tasks().insert(tasklist='@default', body=task).execute()

    # ✅ Also schedule on calendar as a reminder
    add_task_reminder(title, due_date)

    return result.get('id')

def add_task_reminder(title, due_date):
    from calendar_utils import create_event
    details = {
        'purpose': f"Reminder: {title}",
        'description': f"Reminder to complete: {title}",
        'date_time': due_date,
        'attendees': [DEFAULT_ATTENDEE],
        'platform': "Google Calendar"
    }
    return create_event(details, include_meet=False)

def get_upcoming_tasks():
    service = get_tasks_service()
    now = datetime.datetime.utcnow().isoformat() + 'Z'

    results = service.tasks().list(
        tasklist='@default',
        showCompleted=False,
        maxResults=10,
        dueMin=now
    ).execute()

    tasks = results.get('items', [])
    tasks.sort(key=lambda t: t.get('due', '9999-12-31'))
    return [(t['title'], t.get('due', 'No Due Date')) for t in tasks]

def delete_task(task_id):
    service = get_tasks_service()
    service.tasks().delete(tasklist='@default', task=task_id).execute()
    return f"Task {task_id} deleted."

def update_task(task_id, new_title=None, new_due_date=None):
    service = get_tasks_service()
    task = service.tasks().get(tasklist='@default', task=task_id).execute()

    if new_title:
        task['title'] = new_title
    if new_due_date:
        task['due'] = parse_datetime(new_due_date).isoformat() + 'Z'

    updated_task = service.tasks().update(tasklist='@default', task=task_id, body=task).execute()
    return updated_task

def find_task_id_by_title(title_query):
    service = get_tasks_service()
    results = service.tasks().list(tasklist='@default').execute()
    tasks = results.get('items', [])

    for task in tasks:
        if title_query.lower() in task.get('title', '').lower():
            return task['id']
    return None

def mark_task_complete_by_title(title_query):
    service = get_tasks_service()
    tasks = service.tasks().list(tasklist='@default').execute().get('items', [])

    for task in tasks:
        if title_query.lower() in task.get('title', '').lower():
            task['status'] = 'completed'
            updated = service.tasks().update(tasklist='@default', task=task['id'], body=task).execute()
            return updated
    return None