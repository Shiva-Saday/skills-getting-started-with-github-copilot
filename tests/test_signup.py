from urllib.parse import quote

import src.app as app_module


def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    endpoint = f"/activities/{quote(activity_name, safe='')}/signup"
    assert email not in app_module.activities[activity_name]["participants"]

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"
    endpoint = f"/activities/{quote(activity_name, safe='')}/signup"

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_returns_not_found_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"
    endpoint = f"/activities/{quote(activity_name, safe='')}/signup"

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
