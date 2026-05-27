"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Team-based basketball practice and games",
        "schedule": "Tuesdays and Thursdays, 5:00 PM - 6:30 PM",
        "max_participants": 18,
        "participants": ["liam@mergington.edu", "chloe@mergington.edu"]
    },
    "Soccer Club": {
        "description": "Soccer training, drills, and friendly matches",
        "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["noah@mergington.edu", "ava@mergington.edu"]
    },
    "Math Club": {
        "description": "Explore math problems, puzzles, and competitions",
        "schedule": "Mondays, 4:00 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ethan@mergington.edu", "mia@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Prepare for science competitions with hands-on experiments",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["lucas@mergington.edu", "isabella@mergington.edu"]
    },
    "Art Workshop": {
        "description": "Create paintings, drawings, and mixed media art projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["sophia@mergington.edu", "jack@mergington.edu"]
    },
    "Music Ensemble": {
        "description": "Practice instruments and perform music together",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "oliver@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Normalize email for case-insensitive comparison and storage
    normalized = email.lower()
    participants_lower = [p.lower() for p in activity["participants"]]

    # Prevent duplicate signups (case-insensitive)
    if normalized in participants_lower:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Add student (store normalized email to enforce uniqueness)
    activity["participants"].append(normalized)
    return {"message": f"Signed up {normalized} for {activity_name}"}


@app.post("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    # Case-insensitive lookup to find the stored participant
    normalized = email.lower()
    match = None
    for p in activity["participants"]:
        if p.lower() == normalized:
            match = p
            break

    # Ensure student is registered
    if match is None:
        raise HTTPException(status_code=400, detail="Student not registered for this activity")

    activity["participants"].remove(match)
    return {"message": f"Unregistered {match} from {activity_name}"}
