"""Tests for the POST /activities/{activity_name}/signup endpoint"""


def test_successful_signup(client):
    """
    Arrange: Gym Class has no participants, new student ready to sign up
    Act: Make POST request to sign up student
    Assert: Verify successful signup and participant list updated
    """
    # Arrange
    activity_name = "Gym Class"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert f"Signed up {email}" in data["message"]
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email in activities_data[activity_name]["participants"]


def test_multiple_signups_same_activity(client):
    """
    Arrange: Two different students ready to sign up for same activity
    Act: Make two POST signup requests
    Assert: Verify both participants added successfully
    """
    # Arrange
    activity_name = "Gym Class"
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    
    # Act
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email1}
    )
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email2}
    )
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email1 in activities_data[activity_name]["participants"]
    assert email2 in activities_data[activity_name]["participants"]


def test_duplicate_signup_rejected(client):
    """
    Arrange: Student already registered for Chess Club
    Act: Attempt to sign up the same student again
    Assert: Request rejected with 400 status and appropriate error message
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered in fixture
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "Already signed up" in data["detail"]


def test_signup_nonexistent_activity(client):
    """
    Arrange: Activity name doesn't exist in system
    Act: Attempt to sign up for nonexistent activity
    Assert: Request rejected with 404 status
    """
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_missing_email_parameter(client):
    """
    Arrange: Signup request without email parameter
    Act: Make POST request without email query param
    Assert: Request fails appropriately
    """
    # Arrange
    activity_name = "Gym Class"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup")
    
    # Assert
    assert response.status_code in [400, 422]  # Bad request or validation error


def test_signup_empty_email(client):
    """
    Arrange: Signup request with empty email string
    Act: Make POST request with empty email
    Assert: Request processes (FastAPI allows it, but validates server-side)
    """
    # Arrange
    activity_name = "Gym Class"
    email = ""
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    # Even with empty email, the endpoint will accept it (no validation on our end)
    assert response.status_code == 200
