# SmartScheduler

**SmartScheduler** is an AI-powered assistant that automates scheduling meetings, managing tasks, and handling calendar events through natural language. By leveraging Large Language Models (LLMs), SmartSchedulerGPT allows users to schedule, update, delete, and reschedule meetings effortlessly using simple text prompts.

The application now includes integration with **Gemini Flash**, an advanced AI model for enhanced natural language understanding and processing.

---

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Natural Language Meeting Scheduling**: Schedule meetings by simply describing them in natural language.
- **Automatic Event Creation**: Extracts details such as attendees, time, platform, and purpose from user inputs and creates Google Calendar events.
- **Event and Task Management**: Easily manage tasks and events, including adding, updating, and deleting them.
- **Rescheduling Meetings**: Update an existing meeting's time, date, or details.
- **New Meeting Creation with Attendees**: Create new meetings with specific attendees, platforms, and purposes based on natural language input.
- **Gemini Flash Integration**: Uses the Gemini Flash model for improved text understanding, event handling, and natural language processing, ensuring more accurate parsing and handling of scheduling requests.
- **Cross-Platform Integration**: Integrated with Google Calendar API for seamless event creation and management.
- **Time Zone Handling**: Automatically adjusts for different time zones based on user input.

---

## Technologies Used

- **Python**: The core programming language.
- **Gemini Flash Model**: Enhanced AI model for advanced natural language understanding, ensuring more accurate scheduling and task management.
- **Google Calendar API**: For creating, updating, deleting, and managing events on Google Calendar.

---

## Installation

To install and run **SmartSchedulerGPT** locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Sreemurali1/Smart-Schedular---AI.git
   cd smartscheduler-gpt

2. **Install required dependencies:**

   ```bash
   pip install -r requirements.txt

3. **Set up Google Calendar API:**

      - Go to Google Cloud Console.
      
      - Enable the Google Calendar API.
      
      - Set up OAuth 2.0 credentials and download the credentials.json file.
      
      - Place the credentials.json file in the root of the project.

4. **Integrate Gemini Flash Model:**

      - Obtain API access or model weights for the Gemini Flash model.
        
      - Install any necessary dependencies for the Gemini Flash integration.
      
      - Update the integration script to connect the application with Gemini Flash.
  
## Use Cases

### 1. **Create a Meeting**

- **Example 1**: 
    - **Input**: "Schedule a meeting with John tomorrow at 10 AM on Zoom."
    - **Action**: Creates a new event for tomorrow at 10 AM with John on Zoom.

- **Example 2**:
    - **Input**: "Create a meeting on Thursday at 2 PM with Sarah and Michael for project discussion."
    - **Action**: Creates a new meeting for Thursday at 2 PM with Sarah and Michael for a project discussion.

### 2. **Update a Meeting**

- **Example 1**: 
    - **Input**: "Update my meeting with John to 11 AM tomorrow."
    - **Action**: Updates the meeting with John to 11 AM tomorrow.

- **Example 2**:
    - **Input**: "Change the Zoom link for the project discussion meeting."
    - **Action**: Updates the Zoom link for the existing project discussion meeting.

### 3. **Delete a Meeting**

- **Example 1**: 
    - **Input**: "Delete the meeting with John scheduled for tomorrow."
    - **Action**: Deletes the meeting with John scheduled for tomorrow.

- **Example 2**:
    - **Input**: "Remove the project discussion event from my calendar."
    - **Action**: Removes the project discussion event from the calendar.

### 4. **Reschedule a Meeting**

- **Example 1**: 
    - **Input**: "Reschedule my meeting with Sarah and Michael for 3 PM next Wednesday."
    - **Action**: Reschedules the meeting with Sarah and Michael to 3 PM next Wednesday.

- **Example 2**:
    - **Input**: "Change the time of my meeting with John from 10 AM to 12 PM tomorrow."
    - **Action**: Reschedules the meeting with John from 10 AM to 12 PM tomorrow.

### 5. **Create a Meeting with Attendees**

- **Example 1**:
    - **Input**: "Schedule a meeting with John and Jane for a team discussion at 4 PM on Zoom."
    - **Action**: Creates a meeting for a team discussion with John and Jane at 4 PM on Zoom.

- **Example 2**:
    - **Input**: "Create a virtual meeting with Alex, Michael, and Sarah at 2 PM on Google Meet."
    - **Action**: Creates a virtual meeting with Alex, Michael, and Sarah at 2 PM on Google Meet.

### 6. **Event Confirmation**

- **Feature**: Once an event is scheduled, updated, or deleted, a notification will be sent to the user with event details.

## Use Cases

### 1. **Create a Meeting**

- **Example 1**: 
    - **Input**: "Schedule a meeting with John tomorrow at 10 AM on Zoom."
    - **Action**: Creates a new event for tomorrow at 10 AM with John on Zoom.

- **Example 2**:
    - **Input**: "Create a meeting on Thursday at 2 PM with Sarah and Michael for project discussion."
    - **Action**: Creates a new meeting for Thursday at 2 PM with Sarah and Michael for a project discussion.

### 2. **Update a Meeting**

- **Example 1**: 
    - **Input**: "Update my meeting with John to 11 AM tomorrow."
    - **Action**: Updates the meeting with John to 11 AM tomorrow.

- **Example 2**:
    - **Input**: "Change the Zoom link for the project discussion meeting."
    - **Action**: Updates the Zoom link for the existing project discussion meeting.

### 3. **Delete a Meeting**

- **Example 1**: 
    - **Input**: "Delete the meeting with John scheduled for tomorrow."
    - **Action**: Deletes the meeting with John scheduled for tomorrow.

- **Example 2**:
    - **Input**: "Remove the project discussion event from my calendar."
    - **Action**: Removes the project discussion event from the calendar.

### 4. **Reschedule a Meeting**

- **Example 1**: 
    - **Input**: "Reschedule my meeting with Sarah and Michael for 3 PM next Wednesday."
    - **Action**: Reschedules the meeting with Sarah and Michael to 3 PM next Wednesday.

- **Example 2**:
    - **Input**: "Change the time of my meeting with John from 10 AM to 12 PM tomorrow."
    - **Action**: Reschedules the meeting with John from 10 AM to 12 PM tomorrow.

### 5. **Create a Meeting with Attendees**

- **Example 1**:
    - **Input**: "Schedule a meeting with John and Jane for a team discussion at 4 PM on Zoom."
    - **Action**: Creates a meeting for a team discussion with John and Jane at 4 PM on Zoom.

- **Example 2**:
    - **Input**: "Create a virtual meeting with Alex, Michael, and Sarah at 2 PM on Google Meet."
    - **Action**: Creates a virtual meeting with Alex, Michael, and Sarah at 2 PM on Google Meet.

### 6. **Event Confirmation**

- **Feature**: Once an event is scheduled, updated, or deleted, a notification will be sent to the user with event details.

### **Video Demo**
Watch the video demonstration of how SmartSchedulerGPT works:
https://github.com/user-attachments/assets/ac544907-6275-4a50-a4bf-c0cbc60642a1

