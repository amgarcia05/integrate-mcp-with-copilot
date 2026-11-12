# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Teacher login to register and unregister students

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   export TEACHER_CREDENTIALS='{"teacher1":"replace-with-a-strong-password"}'
   uvicorn app:app --reload
   ```

   Set `TEACHER_CREDENTIALS` to a JSON object mapping each teacher username to a strong password. Keep these credentials in your environment or secret manager; do not commit them to the repository. The app returns an error for teacher-only actions if this setting is missing or invalid.

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| GET    | `/auth/teacher`                                                    | Verify teacher credentials using HTTP Basic authentication          |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Register a student (teacher authentication required)                |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Unregister a student (teacher authentication required)            |

Activity viewing remains public. Teacher credentials are held only in the browser's current page session; use HTTPS when serving the app outside localhost.
## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.
