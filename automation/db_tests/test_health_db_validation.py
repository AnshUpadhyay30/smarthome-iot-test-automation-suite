import pytest


@pytest.mark.db
def test_low_wifi_status_updated_in_database(api_client, auth_headers, db_client):
    response = api_client.post(
        "/api/devices/1/simulate-error",
        json={"error_type": "LOW_WIFI"},
        headers=auth_headers
    )

    assert response.status_code == 200

    device = db_client.get_device_by_id(1)

    assert device["health_status"] == "WARNING"
    assert device["error_code"] == "E101"
    assert device["wifi_signal"] == "LOW"


@pytest.mark.db
def test_sensor_failure_updated_in_database(api_client, auth_headers, db_client):
    response = api_client.post(
        "/api/devices/2/simulate-error",
        json={"error_type": "SENSOR_FAILURE"},
        headers=auth_headers
    )

    assert response.status_code == 200

    device = db_client.get_device_by_id(2)

    assert device["health_status"] == "CRITICAL"
    assert device["error_code"] == "E202"


@pytest.mark.db
def test_offline_status_updated_in_database(api_client, auth_headers, db_client):
    response = api_client.post(
        "/api/devices/3/simulate-error",
        json={"error_type": "OFFLINE"},
        headers=auth_headers
    )

    assert response.status_code == 200

    device = db_client.get_device_by_id(3)

    assert device["health_status"] == "OFFLINE"
    assert device["error_code"] == "E303"
    assert device["wifi_signal"] == "NONE"
    assert device["status"] == "OFFLINE"


@pytest.mark.db
def test_clear_error_updates_database(api_client, auth_headers, db_client):
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

    device = db_client.get_device_by_id(1)

    assert device["health_status"] == "HEALTHY"
    assert device["error_code"] is None
    assert device["wifi_signal"] == "GOOD"
    assert device["status"] == "ONLINE"


@pytest.mark.db
def test_simulate_error_creates_audit_log(api_client, auth_headers, db_client):
    response = api_client.post(
        "/api/devices/4/simulate-error",
        json={"error_type": "LOW_WIFI"},
        headers=auth_headers
    )

    assert response.status_code == 200

    latest_log = db_client.get_latest_audit_log_by_device(4)

    assert latest_log is not None
    assert latest_log["action"] == "DEVICE_ERROR_SIMULATED"
    assert latest_log["new_value"] == "WARNING"


@pytest.mark.db
def test_clear_error_creates_audit_log(api_client, auth_headers, db_client):
    api_client.post(
        "/api/devices/4/simulate-error",
        json={"error_type": "LOW_WIFI"},
        headers=auth_headers
    )

    response = api_client.post(
        "/api/devices/4/clear-error",
        headers=auth_headers
    )

    assert response.status_code == 200

    latest_log = db_client.get_latest_audit_log_by_device(4)

    assert latest_log is not None
    assert latest_log["action"] == "DEVICE_ERROR_CLEARED"
    assert latest_log["new_value"] == "HEALTHY"