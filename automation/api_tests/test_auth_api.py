import pytest


@pytest.mark.api
@pytest.mark.smoke
def test_login_success(api_client):
    response = api_client.post(
        "/api/auth/login",
        json={
            "email": "admin@test.com",
            "password": "admin123"
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Login successful"
    assert "token" in data
    assert data["user"]["email"] == "admin@test.com"


@pytest.mark.api
@pytest.mark.negative
def test_login_invalid_password(api_client):
    response = api_client.post(
        "/api/auth/login",
        json={
            "email": "admin@test.com",
            "password": "wrongpass"
        }
    )

    assert response.status_code == 401
    assert response.json()["message"] == "Invalid email or password"


@pytest.mark.api
@pytest.mark.negative
def test_login_missing_email(api_client):
    response = api_client.post(
        "/api/auth/login",
        json={
            "password": "admin123"
        }
    )

    assert response.status_code == 400
    assert response.json()["message"] == "Email and password are required"