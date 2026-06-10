from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities_returns_all_activities():
    # Arrange
    expected_key = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert expected_key in payload
    assert isinstance(payload[expected_key]["participants"], list)


def test_signup_adds_new_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "new_student_signup@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    get_response = client.get("/activities")
    assert email in get_response.json()[activity_name]["participants"]


def test_duplicate_signup_returns_400():
    # Arrange
    activity_name = "Programming Class"
    email = "duplicate_test@example.com"

    # Act
    first_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    second_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up"


def test_delete_removes_participant():
    # Arrange
    activity_name = "Gym Class"
    email = "remove_test@example.com"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"

    get_response = client.get("/activities")
    assert email not in get_response.json()[activity_name]["participants"]
