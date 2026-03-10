"""Tests for DELETE /activities/{activity_name}/unregister endpoint using AAA pattern"""

import pytest


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_successful(self, client, existing_activity, existing_participant):
        """Should successfully unregister an existing student from an activity"""
        # Arrange
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[existing_activity]["participants"])
        assert existing_participant in initial_response.json()[existing_activity]["participants"]

        # Act
        response = client.delete(
            f"/activities/{existing_activity}/unregister",
            params={"email": existing_participant}
        )

        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert existing_participant in response.json()["message"]
        
        # Verify participant was actually removed
        updated_response = client.get("/activities")
        updated_count = len(updated_response.json()[existing_activity]["participants"])
        assert updated_count == initial_count - 1
        assert existing_participant not in updated_response.json()[existing_activity]["participants"]

    def test_unregister_nonexistent_activity(self, client, sample_email, nonexistent_activity):
        """Should return 404 when unregistering from non-existent activity"""
        # Arrange & Act
        response = client.delete(
            f"/activities/{nonexistent_activity}/unregister",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_not_registered(self, client, existing_activity, sample_email):
        """Should return 400 when trying to unregister a student who is not registered"""
        # Arrange & Act
        response = client.delete(
            f"/activities/{existing_activity}/unregister",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]
        
        # Verify participant count did not change
        activity_response = client.get("/activities")
        assert sample_email not in activity_response.json()[existing_activity]["participants"]

    def test_unregister_returns_correct_message(self, client, existing_activity, existing_participant):
        """Should return a message confirming the unregister with email and activity name"""
        # Arrange & Act
        response = client.delete(
            f"/activities/{existing_activity}/unregister",
            params={"email": existing_participant}
        )

        # Assert
        message = response.json()["message"]
        assert existing_participant in message
        assert existing_activity in message
