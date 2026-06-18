from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture(autouse=True)
def restore_activities():
    original_activities = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_activities)


def test_signup_rejects_duplicate_email_after_normalization():
    client = TestClient(app)

    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "  Michael@Mergington.edu "},
    )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "Student is already signed up for this activity"
    }
    assert activities["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_unregister_removes_existing_participant_after_normalization():
    client = TestClient(app)

    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "  Michael@Mergington.edu "},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Removed michael@mergington.edu from Chess Club"
    }
    assert activities["Chess Club"]["participants"] == [
        "daniel@mergington.edu",
    ]