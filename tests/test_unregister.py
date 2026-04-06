from urllib.parse import quote

import src.app as app_module


def test_unregister_removes_existing_participant(client):
    # Arrange
    activity_name = "Gym Class"
    email = "john@mergington.edu"
    endpoint = f"/activities/{quote(activity_name, safe='')}/signup"
    assert email in app_module.activities[activity_name]["participants"]

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_rejects_non_member(client):
    # Arrange
    activity_name = "Tennis Club"
    email = "not.registered@mergington.edu"
    endpoint = f"/activities/{quote(activity_name, safe='')}/signup"
    assert email not in app_module.activities[activity_name]["participants"]

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_returns_not_found_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"
    endpoint = f"/activities/{quote(activity_name, safe='')}/signup"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
