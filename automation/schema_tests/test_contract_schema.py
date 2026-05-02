import pytest
from jsonschema import validate

from schemas.api_schemas import (
    LOGIN_SUCCESS_SCHEMA,
    ERROR_RESPONSE_SCHEMA,
    DEVICES_LIST_SCHEMA,
    DEVICE_DETAIL_SCHEMA,
    DEVICE_UPDATE_RESPONSE_SCHEMA,
    AUDIT_LOGS_RESPONSE_SCHEMA,
    FIRMWARE_LATEST_SCHEMA,
    DEVICE_FIRMWARE_SCHEMA,
    FIRMWARE_UPDATE_SCHEMA,
    HEALTH_RESPONSE_SCHEMA,
    HEALTH_ACTION_RESPONSE_SCHEMA
)


@pytest.mark.schema
def test_login_success_response_schema(api_client):
    response = api_client.post(
        "/api/auth/login",
        json={
            "email": "admin@test.com",
            "password": "admin123"
        }
    )

    assert response.status_code == 200
    validate(instance=response.json(), schema=LOGIN_SUCCESS_SCHEMA)


@pytest.mark.schema
def test_login_error_response_schema(api_client):
    response = api_client.post(
        "/api/auth/login",
        json={
            "email": "admin@test.com",
            "password": "wrongpass"
        }
    )

    assert response.status_code == 401
    validate(instance=response.json(), schema=ERROR_RESPONSE_SCHEMA)


@pytest.mark.schema
def test_devices_list_response_schema(api_client, auth_headers):
    response = api_client.get(
        "/api/devices",
        headers=auth_headers
    )

    assert response.status_code == 200
    validate(instance=response.json(), schema=DEVICES_LIST_SCHEMA)


@pytest.mark.schema
def test_device_detail_response_schema(api_client, auth_headers):
    response = api_client.get(
        "/api/devices/1",
        headers=auth_headers
    )

    assert response.status_code == 200
    validate(instance=response.json(), schema=DEVICE_DETAIL_SCHEMA)


@pytest.mark.schema
def test_device_not_found_error_schema(api_client, auth_headers):
    response = api_client.get(
        "/api/devices/999",
        headers=auth_headers
    )

    assert response.status_code == 404
    validate(instance=response.json(), schema=ERROR_RESPONSE_SCHEMA)


@pytest.mark.schema
def test_power_update_response_schema(api_client, auth_headers):
    response = api_client.patch(
        "/api/devices/1/power",
        json={"power": "ON"},
        headers=auth_headers
    )

    assert response.status_code == 200
    validate(instance=response.json(), schema=DEVICE_UPDATE_RESPONSE_SCHEMA)


@pytest.mark.schema
def test_temperature_update_response_schema(api_client, auth_headers):
    response = api_client.patch(
        "/api/devices/1/temperature",
        json={"temperature": 25},
        headers=auth_headers
    )

    assert response.status_code == 200
    validate(instance=response.json(), schema=DEVICE_UPDATE_RESPONSE_SCHEMA)


@pytest.mark.schema
def test_volume_update_response_schema(api_client, auth_headers):
    response = api_client.patch(
        "/api/devices/2/volume",
        json={"volume": 55},
        headers=auth_headers
    )

    assert response.status_code == 200
    validate(instance=response.json(), schema=DEVICE_UPDATE_RESPONSE_SCHEMA)


@pytest.mark.schema
def test_cycle_update_response_schema(api_client, auth_headers):
    response = api_client.patch(
        "/api/devices/4/cycle",
        json={
            "cycle_status": "START",
            "water_level": 3
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    validate(instance=response.json(), schema=DEVICE_UPDATE_RESPONSE_SCHEMA)


@pytest.mark.schema
def test_audit_logs_response_schema(api_client, auth_headers):
    response = api_client.get(
        "/api/audit-logs",
        headers=auth_headers
    )

    assert response.status_code == 200
    validate(instance=response.json(), schema=AUDIT_LOGS_RESPONSE_SCHEMA)


@pytest.mark.schema
def test_latest_firmware_response_schema(api_client, auth_headers):
    response = api_client.get(
        "/api/firmware/latest/AC",
        headers=auth_headers
    )

    assert response.status_code == 200
    validate(instance=response.json(), schema=FIRMWARE_LATEST_SCHEMA)


@pytest.mark.schema
def test_device_firmware_response_schema(api_client, auth_headers):
    response = api_client.get(
        "/api/devices/1/firmware",
        headers=auth_headers
    )

    assert response.status_code == 200
    validate(instance=response.json(), schema=DEVICE_FIRMWARE_SCHEMA)


@pytest.mark.schema
def test_firmware_update_response_schema(api_client, auth_headers):
    response = api_client.post(
        "/api/devices/1/firmware/update",
        json={"firmware_version": "1.1.0"},
        headers=auth_headers
    )

    assert response.status_code == 200
    validate(instance=response.json(), schema=FIRMWARE_UPDATE_SCHEMA)


@pytest.mark.schema
def test_health_response_schema(api_client, auth_headers):
    response = api_client.get(
        "/api/devices/1/health",
        headers=auth_headers
    )

    assert response.status_code == 200
    validate(instance=response.json(), schema=HEALTH_RESPONSE_SCHEMA)


@pytest.mark.schema
def test_simulate_error_response_schema(api_client, auth_headers):
    response = api_client.post(
        "/api/devices/1/simulate-error",
        json={"error_type": "LOW_WIFI"},
        headers=auth_headers
    )

    assert response.status_code == 200
    validate(instance=response.json(), schema=HEALTH_ACTION_RESPONSE_SCHEMA)


@pytest.mark.schema
def test_clear_error_response_schema(api_client, auth_headers):
    response = api_client.post(
        "/api/devices/1/clear-error",
        headers=auth_headers
    )

    assert response.status_code == 200
    validate(instance=response.json(), schema=HEALTH_ACTION_RESPONSE_SCHEMA)