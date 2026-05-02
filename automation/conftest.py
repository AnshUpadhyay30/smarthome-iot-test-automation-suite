import subprocess
import sys
from pathlib import Path

import pytest
from utils.api_client import APIClient
from utils.db_client import DBClient


@pytest.fixture(scope="session", autouse=True)
def reset_database_before_test_session():
    """
    Full test run start hone se pehle database ko clean seed state me le aata hai.
    Isse tests ek dusre ke state ko break nahi karte.
    """
    project_root = Path(__file__).resolve().parents[1]
    seed_file = project_root / "backend" / "seed.py"
    migrate_file = project_root / "backend" / "migrate_health_columns.py"

    subprocess.run([sys.executable, str(seed_file)], check=True)
    subprocess.run([sys.executable, str(migrate_file)], check=True)


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