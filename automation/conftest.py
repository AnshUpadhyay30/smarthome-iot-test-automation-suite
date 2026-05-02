import pytest
from utils.api_client import APIClient
from utils.db_client import DBClient


@pytest.fixture(scope="session")
def api_client():
    return APIClient()


@pytest.fixture(scope="session")
def auth_token(api_client):
    response = api_client.post(
        "/api/auth/login",
        json={
            "email": "admin@test.com",
            "password": "admin123"
        }
    )

    assert response.status_code == 200

    data = response.json()
    return data["token"]


@pytest.fixture(scope="session")
def auth_headers(auth_token):
    return {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }


@pytest.fixture()
def db_client():
    return DBClient()