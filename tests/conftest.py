"""Shared fixtures for API tests using AAA (Arrange-Act-Assert) pattern"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Arrange: Provide a test client for API calls with fresh state"""
    # Reset activities to initial state before each test
    initial_activities = {
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
        "Debate Club": {
            "description": "Develop argumentation and public speaking skills",
            "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["alex@mergington.edu"]
        },
        "Math Olympiad": {
            "description": "Problem-solving and advanced mathematics competition",
            "schedule": "Saturdays, 10:00 AM - 12:00 PM",
            "max_participants": 15,
            "participants": ["kevin@mergington.edu", "sarah@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball with regular tournaments",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu", "tyler@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Tennis training and friendly matches",
            "schedule": "Tuesdays and Fridays, 3:30 PM - 4:30 PM",
            "max_participants": 16,
            "participants": ["grace@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and mixed media techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu", "luna@mergington.edu"]
        },
        "Music Ensemble": {
            "description": "Play instruments and perform in concerts",
            "schedule": "Mondays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["noah@mergington.edu"]
        }
    }
    
    # Clear and rebuild activities dict
    activities.clear()
    activities.update(initial_activities)
    
    return TestClient(app)


@pytest.fixture
def sample_email():
    """Arrange: Provide a sample email for testing"""
    return "test.student@mergington.edu"


@pytest.fixture
def existing_activity():
    """Arrange: Provide an existing activity name"""
    return "Chess Club"


@pytest.fixture
def existing_participant():
    """Arrange: Provide an existing participant email"""
    return "michael@mergington.edu"


@pytest.fixture
def nonexistent_activity():
    """Arrange: Provide a non-existent activity name"""
    return "Nonexistent Club"

