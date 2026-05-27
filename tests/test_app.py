def test_root_redirects_to_index(client):
    # Arrange: nothing special (client fixture provides app)
    # Act
    response = client.get("/", follow_redirects=False)
    # Assert
    assert response.status_code in (307, 302)
    assert response.headers["location"].endswith("/static/index.html")


def test_get_activities_returns_map(client):
    # Arrange
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success_adds_normalized_email(client):
    # Arrange
    activity = "Chess Club"
    email = "NewStudent@Mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "signed up" in data["message"].lower()
    # Verify normalized addition
    activities = client.get("/activities").json()
    assert email.lower() in [p.lower() for p in activities[activity]["participants"]]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity = "Chess Club"
    existing = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": existing.upper()})

    # Assert
    assert response.status_code == 400


def test_signup_activity_not_found_returns_404(client):
    # Arrange
    activity = "Nonexistent"
    email = "student@example.com"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404


def test_unregister_success_removes_participant(client):
    # Arrange
    activity = "Chess Club"
    to_remove = "daniel@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/unregister", params={"email": to_remove})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "unregistered" in data["message"].lower()
    activities = client.get("/activities").json()
    assert to_remove.lower() not in [p.lower() for p in activities[activity]["participants"]]


def test_unregister_not_registered_returns_400(client):
    # Arrange
    activity = "Chess Club"
    email = "notregistered@example.com"

    # Act
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 400


def test_unregister_activity_not_found_returns_404(client):
    # Arrange
    activity = "NopeClub"
    email = "student@example.com"

    # Act
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 404
