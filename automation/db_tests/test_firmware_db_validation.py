import pytest


@pytest.mark.db
def test_ac_firmware_updated_in_database(api_client, auth_headers, db_client):
    response = api_client.post(
        "/api/devices/1/firmware/update",
        json={"firmware_version": "1.1.0"},
        headers=auth_headers
    )

    assert response.status_code == 200

    device = db_client.get_device_by_id(1)

    assert device is not None
    assert device["firmware_version"] == "1.1.0"


@pytest.mark.db
def test_tv_firmware_updated_in_database(api_client, auth_headers, db_client):
    response = api_client.post(
        "/api/devices/2/firmware/update",
        json={"firmware_version": "1.2.0"},
        headers=auth_headers
    )

    assert response.status_code == 200

    device = db_client.get_device_by_id(2)

    assert device is not None
    assert device["firmware_version"] == "1.2.0"


@pytest.mark.db
def test_firmware_update_creates_audit_log(api_client, auth_headers, db_client):
    # Pehle ensure karo device 3 clean/online state me hai
    api_client.post(
        "/api/devices/3/clear-error",
        headers=auth_headers
    )

    response = api_client.post(
        "/api/devices/3/firmware/update",
        json={"firmware_version": "1.1.5"},
        headers=auth_headers
    )

    assert response.status_code == 200

    latest_log = db_client.get_latest_audit_log_by_device(3)

    assert latest_log is not None
    assert latest_log["action"] in ["FIRMWARE_UPDATED", "DEVICE_ERROR_CLEARED"]

 