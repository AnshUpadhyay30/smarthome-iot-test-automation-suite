import pytest


@pytest.mark.api
@pytest.mark.smoke
def test_get_devices_success(api_client, auth_headers):
    response = api_client.get(
        "/api/devices",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()
    assert "devices" in data
    assert len(data["devices"]) == 4


@pytest.mark.api
@pytest.mark.negative
def test_get_devices_without_token(api_client):
    response = api_client.get("/api/devices")

    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized. Valid token required."


@pytest.mark.api
def test_get_device_detail_success(api_client, auth_headers):
    response = api_client.get(
        "/api/devices/1",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()
    assert data["device"]["id"] == 1
    assert data["device"]["type"] == "AC"


@pytest.mark.api
@pytest.mark.negative
def test_get_invalid_device_detail(api_client, auth_headers):
    response = api_client.get(
        "/api/devices/999",
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json()["message"] == "Device not found"


@pytest.mark.api
def test_update_ac_power_success(api_client, auth_headers):
    response = api_client.patch(
        "/api/devices/1/power",
        json={"power": "ON"},
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["device"]["power"] == "ON"


@pytest.mark.api
def test_update_tv_volume_success(api_client, auth_headers):
    response = api_client.patch(
        "/api/devices/2/volume",
        json={"volume": 60},
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["device"]["volume"] == 60


@pytest.mark.api
def test_update_refrigerator_temperature_success(api_client, auth_headers):
    response = api_client.patch(
        "/api/devices/3/temperature",
        json={
            "temperature": 5,
            "freezer_temperature": -20
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["device"]["temperature"] == 5
    assert response.json()["device"]["freezer_temperature"] == -20


@pytest.mark.api
def test_update_washing_machine_cycle_success(api_client, auth_headers):
    response = api_client.patch(
        "/api/devices/4/cycle",
        json={
            "cycle_status": "START",
            "water_level": 4
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["device"]["cycle_status"] == "START"
    assert response.json()["device"]["water_level"] == 4


@pytest.mark.api
def test_audit_logs_success(api_client, auth_headers):
    response = api_client.get(
        "/api/audit-logs",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert "audit_logs" in response.json()