"""Tests for the GET /activities endpoint"""


def test_get_all_activities(client):
    """
    Arrange: No setup needed, using default activities from conftest
    Act: Make GET request to /activities
    Assert: Verify response status and structure
    """
    # Arrange
    expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    for activity_name in expected_activities:
        assert activity_name in data


def test_activity_has_required_fields(client):
    """
    Arrange: No setup needed, using default activities from conftest
    Act: Make GET request and check activity structure
    Assert: Verify each activity has all required fields
    """
    # Arrange
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    for activity_name, activity_details in data.items():
        for field in required_fields:
            assert field in activity_details, f"{activity_name} missing {field}"


def test_participants_list_returned(client):
    """
    Arrange: Chess Club has 2 participants from fixture
    Act: Make GET request to /activities
    Assert: Verify participants list is returned correctly
    """
    # Arrange
    expected_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert data["Chess Club"]["participants"] == expected_participants


def test_empty_participants_list(client):
    """
    Arrange: Gym Class has no participants from fixture
    Act: Make GET request to /activities
    Assert: Verify empty participants list is returned
    """
    # Arrange
    activity_name = "Gym Class"
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert data[activity_name]["participants"] == []
    assert len(data[activity_name]["participants"]) == 0
