"""Tests for GET /activities endpoint using AAA (Arrange-Act-Assert) pattern"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client):
        """Should return list of all activities with correct structure"""
        # Arrange
        expected_keys = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) > 0
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert set(activity_data.keys()) == expected_keys
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)

    def test_get_activities_chess_club_exists(self, client):
        """Should include Chess Club activity in response"""
        # Arrange & Act
        response = client.get("/activities")

        # Assert
        activities = response.json()
        assert "Chess Club" in activities
        assert activities["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"

    def test_get_activities_participants_are_lists(self, client):
        """Should ensure all participant lists are properly formatted"""
        # Arrange & Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list)
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert "@" in participant  # Verify email format
