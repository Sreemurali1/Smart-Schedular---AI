import datetime

from prompt_parser import extract_meeting_details
from calendar_utils import (
    create_event,
    force_reschedule_by_email_and_purpose,
    get_calendar_service,
    get_task_reminder_events
)
from task_utils import (
    create_google_task,
    add_task_reminder,
    delete_task,
    update_task,
    find_task_id_by_title,
    mark_task_complete_by_title,
    get_tasks_service
)

def main():
    print("\n📅 Welcome to SmartSchedulerGPT!")
    user_input = input("📝 Describe what you'd like to do (e.g., 'Schedule meeting with John on Friday' or 'Add task to submit report by Monday'): ").strip()

    parsed_response = extract_meeting_details(user_input)

    if not parsed_response:
        print("❌ Failed to parse input. Please try again.")
        return

    meeting_details = parsed_response.get("meeting_details")
    print("Parsed meeting details:", meeting_details)
    task_details = parsed_response.get("task_details")
    action = parsed_response.get("action")
    confirmation_message = parsed_response.get("confirmation_message", "Action completed successfully.")

    # ✅ Fallback for "show upcoming tasks" if Gemini missed it
    if not action and "show" in user_input.lower() and "task" in user_input.lower():
        action = "show"
        confirmation_message = "Here are your upcoming tasks!"

    if action == "daily_summary":
        print("\n🗓️ Here's your schedule for today:\n")

        now = datetime.datetime.utcnow()
        start = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
        end = now.replace(hour=23, minute=59, second=59).isoformat() + 'Z'

        calendar_service = get_calendar_service()
        tasks_service = get_tasks_service()

        events = calendar_service.events().list(
            calendarId='primary',
            timeMin=start,
            timeMax=end,
            singleEvents=True,
            orderBy='startTime'
        ).execute().get('items', [])

        tasks = tasks_service.tasks().list(
            tasklist='@default',
            showCompleted=False,
            dueMax=end
        ).execute().get('items', [])

        if not events and not tasks:
            print("📭 You have no events or tasks scheduled for today.")
            return

        if events:
            print(f"📅 You have {len(events)} meeting(s):")
            for event in events:
                summary = event.get('summary', 'No Title')
                time = event['start'].get('dateTime', event['start'].get('date'))
                try:
                    parsed_time = datetime.datetime.fromisoformat(time.replace("Z", "+00:00"))
                    formatted_time = parsed_time.strftime("%A, %d %b %Y at %I:%M %p")
                except Exception:
                    formatted_time = time
                print(f"- {summary} at {formatted_time}")

        if tasks:
            print(f"\n📝 You have {len(tasks)} task(s):")
            for task in tasks:
                title = task.get('title', 'Untitled')
                due = task.get('due', 'Today')
                try:
                    due_dt = datetime.datetime.fromisoformat(due.replace("Z", "+00:00"))
                    formatted_due = due_dt.strftime("%A, %d %b %Y at %I:%M %p")
                except Exception:
                    formatted_due = due
                print(f"- {title} (Due: {formatted_due})")

        return

    if not meeting_details and not task_details and not action:
        print("❌ Could not extract any valid task or meeting information from your input.")
        return

    try:
        if meeting_details:
            is_reschedule = any(keyword in user_input.lower() for keyword in ["reschedule", "postpone", "change", "move"])
            if is_reschedule:
                attendee_email = meeting_details.get("attendees", [None])[0]
                purpose = meeting_details.get("purpose", "")
                new_datetime = meeting_details.get("date_time", "")

                if not attendee_email or not purpose or not new_datetime:
                    print("❌ Missing details: attendee, purpose, or new date/time.")
                    return

                meeting_link = force_reschedule_by_email_and_purpose(attendee_email, purpose, new_datetime)
                print("\n🔁 Meeting rescheduled successfully!")
            else:
                meeting_link = create_event(meeting_details)
                print("\n✅", confirmation_message)

        elif task_details:
            action = task_details.get("action")

            if action == "add":
                task_id = create_google_task(task_details['title'], task_details['due_date'])
                print("\n✅ Task added. ID:", task_id)

                # ✅ Explicit calendar reminder
                try:
                    reminder_link = add_task_reminder(task_details['title'], task_details['due_date'])
                    if reminder_link:
                        print(f"🔔 Reminder scheduled on calendar: {reminder_link}")
                    else:
                        print("⚠️ Reminder creation failed or returned no link.")
                except Exception as e:
                    print(f"❌ Failed to add reminder to calendar: {e}")

                print("📝", confirmation_message)

            elif action == "update":
                task_title = (
                    task_details.get("updated_fields", {}).get("title")
                    or task_details.get("title")
                )

                if "done" in user_input.lower() or "complete" in user_input.lower():
                    updated = mark_task_complete_by_title(task_title)
                    if updated:
                        print(f"\n✅ Task '{updated['title']}' marked as completed.")
                    else:
                        print("❌ Task not found to mark as complete.")
                    return

                task_id = task_details.get("task_id") or find_task_id_by_title(task_title)
                if not task_id:
                    print("❌ Task ID not found or unable to match task title.")
                    return

                updated = update_task(
                    task_id,
                    new_title=task_details.get('updated_fields', {}).get('title'),
                    new_due_date=task_details.get('updated_fields', {}).get('due_date')
                )
                print("\n✏️ Task updated:", updated['title'])
                print("📝", confirmation_message)

            elif action == "delete":
                task_id = task_details.get('task_id')
                if not task_id:
                    title = task_details.get('title')
                    task_id = find_task_id_by_title(title)
                    if not task_id:
                        print("❌ Task ID not found or unable to match task title.")
                        return
                result = delete_task(task_id)
                print("\n🗑️", result)
                print("📝", confirmation_message)

        if action == "show":
            upcoming = get_task_reminder_events()
            if not upcoming:
                print("\n📭 No upcoming task reminders.")
            else:
                print("\n📋 Upcoming Task Reminders from Calendar:")
                for title, due in upcoming:
                    try:
                        due_dt = datetime.datetime.fromisoformat(due.replace("Z", "+00:00"))
                        formatted_due = due_dt.strftime("%A, %d %b %Y at %I:%M %p")
                    except Exception:
                        formatted_due = due
                    print(f"- {title} (Reminder: {formatted_due})")

    except Exception as e:
        print("\n❌ Failed to process your request:")
        print(e)

if __name__ == "__main__":
    main()
