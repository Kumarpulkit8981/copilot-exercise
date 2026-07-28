import copy
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

import app as app_module


@pytest.fixture(autouse=True)
def restore_activity_state():
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))


@pytest.fixture()
def client():
    with TestClient(app_module.app) as test_client:
        yield test_client


def test_get_activities_returns_catalog(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_signup_for_activity_adds_participant(client):
    email = "backend-test@mergington.edu"
    response = client.post(f"/activities/Programming%20Class/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Programming Class"

    activities = client.get("/activities").json()
    assert email in activities["Programming Class"]["participants"]


def test_unregister_participant_removes_email_from_activity(client):
    email = "backend-remove@mergington.edu"
    client.post(f"/activities/Programming%20Class/signup?email={email}")

    response = client.delete(f"/activities/Programming%20Class/participants/{email}")

    assert response.status_code == 200
    assert "Removed" in response.json()["message"]

    activities = client.get("/activities").json()
    assert email not in activities["Programming Class"]["participants"]


def test_unregister_participant_returns_404_for_unknown_participant(client):
    response = client.delete(
        "/activities/Programming%20Class/participants/unknown@mergington.edu"
    )

    assert response.status_code == 404
