from src.app import activities


def test_signup_rejects_duplicate_email_after_normalization(client):
    # Arrange
    activity_name = "Chess Club"
    email = "  Michael@Mergington.edu "

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 409
    assert response.json() == {
        "detail": "Student is already signed up for this activity"
    }
    assert activities[activity_name]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_adds_new_participant_after_normalization(client):
    # Arrange
    activity_name = "Chess Club"
    email = "  NewStudent@Mergington.edu "

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up newstudent@mergington.edu for Chess Club"
    }
    assert activities[activity_name]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
        "newstudent@mergington.edu",
    ]


def test_unregister_removes_existing_participant_after_normalization(client):
    # Arrange
    activity_name = "Chess Club"
    email = "  Michael@Mergington.edu "

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": "Removed michael@mergington.edu from Chess Club"
    }
    assert activities[activity_name]["participants"] == [
        "daniel@mergington.edu",
    ]


def test_unregister_returns_not_found_for_missing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "nobody@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Student is not signed up for this activity"
    }