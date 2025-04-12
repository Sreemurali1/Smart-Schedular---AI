# extractor.py
import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

def extract_meeting_details(prompt): 
    response = model.generate_content(
        f"""
        You are SmartSchedulerGPT – an AI assistant that understands natural language requests and identifies whether the user is talking about a MEETING, a TASK, or a DAILY SUMMARY.
        Extract the user input accurately, including date and time, and return a JSON object with the relevant details.

        Return a JSON object with these possible keys:
        - "meeting_details" (for meetings)
        - "task_details" (for tasks)
        - "action" (for general commands like showing tasks or today's schedule)
        - "confirmation_message" (a friendly message confirming the action)

        👥 For MEETING requests, include:
        "meeting_details": {{
            "description": string,
            "attendees": [list of names or emails],
            "date_time": string,
            "platform": string (e.g., Zoom, Google Meet),
            "purpose": string
        }}
        After completing a meeting request, add:
        "confirmation_message": "Your meeting details have been saved! Looking forward to it."

        ✅ For TASK requests, include:
        "task_details": {{
            "title": string,
            "due_date": string,
            "category": "work" or "personal",
            "action": "add", "update", "delete", or "show",
            "task_id": string (optional),
            "updated_fields": {{
                "title": string (optional),
                "due_date": string (optional),
                "status": string (optional)
            }}
        }}
        After completing a task request, add:
        "confirmation_message": "Your task has been updated successfully!"

        🗓️ If the user asks for today’s schedule or summary, return:
        {{
            "action": "daily_summary",
            "confirmation_message": "Here’s your schedule for today! Let's get organized."
        }}

        📋 If the user asks to see tasks (e.g., "show tasks", "list upcoming tasks", "what do I need to do"), return:
        {{
            "action": "show",
            "confirmation_message": "Here are your upcoming tasks! Stay on track."
        }}

        ⚠️ If the user says a task is done or complete:
        - Set action to "update"
        - Include the task title
        - Set "status" to "completed" inside "updated_fields"
        After completing a task request, add:
        "confirmation_message": "Well done! Your task is marked as completed."

        Always respond with a valid JSON object. No markdown, no extra explanation.

        Sentence: "{prompt}"
        """
    )



    try:
        text = response.text.strip()
        match = re.search(r'{.*}', text, re.DOTALL)
        if not match:
            raise ValueError("No JSON found in Gemini response")

        parsed = json.loads(match.group())
        return parsed

    except Exception as e:
        print("❌ Error parsing Gemini response:", e)
        print("Raw response:", response.text)
        raise
