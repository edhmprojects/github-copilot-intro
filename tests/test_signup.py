"""Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern"""

import pytest


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_successful(self, client, existing_activity, sample_email):
        """Should successfully sign up a new student for an activity"""
        # Arrange
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[existing_activity]["participants"])

        # Act
        response = client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert sample_email in response.json()["message"]
        
        # Verify participant was actually added
        updated_response = client.get("/activities")
        updated_count = len(updated_response.json()[existing_activity]["participants"])
        assert updated_count == initial_count + 1
        assert sample_email in updated_response.json()[existing_activity]["participants"]

    def test_signup_nonexistent_activity(self, client, sample_email, nonexistent_activity):
        """Should return 404 when signing up for non-existent activity"""
        # Arrange & Act
        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_duplicate_email(self, client, existing_activity, existing_participant):
        """Should return 400 when student tries to sign up twice for same activity"""
        # Arrange
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[existing_activity]["participants"])

        # Act
        response = client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": existing_participant}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
        
        # Verify participant count did not change
        updated_response = client.get("/activities")
        updated_count = len(updated_response.json()[existing_activity]["participants"])
        assert updated_count == initial_count

    def test_signup_returns_correct_message(self, client, existing_activity, sample_email):
        """Should return a message confirming the signup with email and activity name"""
        # Arrange & Act
        response = client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": sample_email}
        )

        # Assert
        message = response.json()["message"]
        assert sample_email in message
        assert existing_activity in message
