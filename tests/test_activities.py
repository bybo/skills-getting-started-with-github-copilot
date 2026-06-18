from src.app import activities


def test_get_root_redirects_to_static_index(client):
    # Arrange

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_seeded_activity_data(client):
    # Arrange
    expected_activities = set(activities.keys())

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200

    payload = response.json()

    assert set(payload.keys()) == expected_activities
    assert payload["Chess Club"]["description"] == activities["Chess Club"]["description"]
    assert payload["Chess Club"]["participants"] == activities["Chess Club"]["participants"]
    assert payload["Basketball Team"]["max_participants"] == 15