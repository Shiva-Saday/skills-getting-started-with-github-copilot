def test_get_activities_returns_expected_shape(client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)
    activities = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(activities, dict)
    assert activities

    for _, details in activities.items():
        assert isinstance(details, dict)
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details
        assert isinstance(details["description"], str)
        assert isinstance(details["schedule"], str)
        assert isinstance(details["max_participants"], int)
        assert isinstance(details["participants"], list)
