import pytest


@pytest.mark.api
def test_get_device_health_success(api_client, auth_headers):
    response = api_client.get(
        "/api/devices/1/health",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()
    assert data["health"]["device_id"] == 1
    assert data["health"]["device_type"] == "AC"
    assert "health_status" in data["health"]
    assert "wifi_signal" in data["health"]
    assert "firmware_outdated" in data["health"]


@pytest.mark.api
def test_get_tv_health_success(api_client, auth_headers):
    response = api_client.get(
        "/api/devices/2/health",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["health"]["device_type"] == "TV"


@pytest.mark.api
@pytest.mark.negative
def test_get_health_without_token(api_client):
    response = api_client.get("/api/devices/1/health")

    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized. Valid token required."


@pytest.mark.api
@pytest.mark.negative
def test_get_health_invalid_device_id(api_client, auth_headers):
    response = api_client.get(
        "/api/devices/999/health",
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json()["message"] == "Device not found"


@pytest.mark.api
def test_simulate_low_wifi_error(api_client, auth_headers):
    response = api_client.post(
        "/api/devices/1/simulate-error",
        json={"error_type": "LOW_WIFI"},
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Device error simulated successfully"
    assert data["health"]["health_status"] == "WARNING"
    assert data["health"]["error_code"] == "E101"
    assert data["health"]["wifi_signal"] == "LOW"


@pytest.mark.api
def test_simulate_sensor_failure_error(api_client, auth_headers):
    response = api_client.post(
        "/api/devices/2/simulate-error",
        json={"error_type": "SENSOR_FAILURE"},
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()
    assert data["health"]["health_status"] == "CRITICAL"
    assert data["health"]["error_code"] == "E202"


@pytest.mark.api
def test_simulate_offline_error(api_client, auth_headers):
    response = api_client.post(
        "/api/devices/3/simulate-error",
        json={"error_type": "OFFLINE"},
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()
    assert data["health"]["health_status"] == "OFFLINE"
    assert data["health"]["error_code"] == "E303"
    assert data["health"]["status"] == "OFFLINE"
    assert data["health"]["wifi_signal"] == "NONE"


@pytest.mark.api
@pytest.mark.negative
def test_simulate_unsupported_error_type(api_client, auth_headers):
    response = api_client.post(
        "/api/devices/1/simulate-error",
        json={"error_type": "BATTERY_LOW"},
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json()["message"] == "Unsupported error type"


@pytest.mark.api
@pytest.mark.negative
def test_simulate_error_invalid_device_id(api_client, auth_headers):
    response = api_client.post(
        "/api/devices/999/simulate-error",
        json={"error_type": "LOW_WIFI"},
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json()["message"] == "Device not found"


@pytest.mark.api
@pytest.mark.negative
def test_simulate_error_without_token(api_client):
    response = api_client.post(
        "/api/devices/1/simulate-error",
        json={"error_type": "LOW_WIFI"}
    )

    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized. Valid token required."


@pytest.mark.api
def test_clear_device_error_success(api_client, auth_headers):
    api_client.post(
        "/api/devices/1/simulate-error",
        json={"error_type": "LOW_WIFI"},
        headers=auth_headers
    )

    response = api_client.post(
        "/api/devices/1/clear-error",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Device error cleared successfully"
    assert data["health"]["health_status"] == "HEALTHY"
    assert data["health"]["error_code"] is None
    assert data["health"]["wifi_signal"] == "GOOD"
    assert data["health"]["status"] == "ONLINE"


@pytest.mark.api
@pytest.mark.negative
def test_clear_error_invalid_device_id(api_client, auth_headers):
    response = api_client.post(
        "/api/devices/999/clear-error",
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json()["message"] == "Device not found"


@pytest.mark.api
@pytest.mark.negative
def test_clear_error_without_token(api_client):
    response = api_client.post("/api/devices/1/clear-error")

    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized. Valid token required."