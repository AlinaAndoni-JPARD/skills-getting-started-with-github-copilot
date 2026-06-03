"""Tests for the DELETE /activities/{activity_name}/unregister endpoint"""


def test_successful_unregister(client):
    """
    Arrange: Michael is registered for Chess Club
    Act: Make DELETE request to unregister student
    Assert: Verify successful unregistration and participant list updated
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered in fixture
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert f"Unregistered {email}" in data["message"]
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email not in activities_data[activity_name]["participants"]


def test_multiple_unregisters(client):
    """
    Arrange: Two students registered for Chess Club
    Act: Unregister both students sequentially
    Assert: Both successfully removed
    """
    # Arrange
    activity_name = "Chess Club"
    email1 = "michael@mergington.edu"
    email2 = "daniel@mergington.edu"
    
    # Act
    response1 = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email1}
    )
    response2 = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email2}
    )
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email1 not in activities_data[activity_name]["participants"]
    assert email2 not in activities_data[activity_name]["participants"]
    assert len(activities_data[activity_name]["participants"]) == 0


def test_unregister_not_registered(client):
    """
    Arrange: Student was never registered for the activity
    Act: Attempt to unregister student not in participants list
    Assert: Request rejected with 404 status
    """
    # Arrange
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Participant not found" in data["detail"]


def test_unregister_nonexistent_activity(client):
    """
    Arrange: Activity doesn't exist
    Act: Attempt to unregister from nonexistent activity
    Assert: Request rejected with 404 status for activity not found
    """
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_empty_activity(client):
    """
    Arrange: Activity with no participants
    Act: Attempt to unregister from activity with no signups
    Assert: Request rejected with 404
    """
    # Arrange
    activity_name = "Gym Class"  # No participants in fixture
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Participant not found" in data["detail"]


def test_unregister_missing_email_parameter(client):
    """
    Arrange: Unregister request without email parameter
    Act: Make DELETE request without email query param
    Assert: Request fails appropriately
    """
    # Arrange
    activity_name = "Chess Club"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/unregister")
    
    # Assert
    assert response.status_code in [400, 422]  # Bad request or validation error


def test_signup_then_unregister_flow(client):
    """
    Arrange: Student starts unregistered for Gym Class
    Act: Sign up, verify signup, then unregister, verify removal
    Assert: Complete signup/unregister flow works correctly
    """
    # Arrange
    activity_name = "Gym Class"
    email = "testflow@mergington.edu"
    
    # Act - Sign up
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert - Signup successful
    assert signup_response.status_code == 200
    activities_after_signup = client.get("/activities").json()
    assert email in activities_after_signup[activity_name]["participants"]
    
    # Act - Unregister
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert - Unregister successful
    assert unregister_response.status_code == 200
    activities_after_unregister = client.get("/activities").json()
    assert email not in activities_after_unregister[activity_name]["participants"]
