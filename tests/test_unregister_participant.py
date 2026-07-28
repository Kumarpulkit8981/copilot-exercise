import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    response = client.delete("/activities/Programming%20Class/participants/emma@mergington.edu")

    assert response.status_code == 200
    data = response.json()
    assert "Removed" in data["message"]

    activities = client.get("/activities").json()
    assert "emma@mergington.edu" not in activities["Programming Class"]["participants"]


def test_unregister_participant_returns_404_for_unknown_participant():
    response = client.delete("/activities/Programming%20Class/participants/unknown@mergington.edu")

    assert response.status_code == 404
