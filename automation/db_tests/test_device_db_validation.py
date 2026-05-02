import pytest


@pytest.mark.db
def test_ac_temperature_updated_in_database(api_client, auth_headers, db_client):
    response = api_client.patch(
        "/api/devices/1/temperature",
        json={"temperature": 25},
        headers=auth_headers
    )

    assert response.status_code == 200

    device = db_client.get_device_by_id(1)

    assert device is not None
    assert device["temperature"] == 25


@pytest.mark.db
def test_tv_volume_updated_in_database(api_client, auth_headers, db_client):
    response = api_client.patch(
        "/api/devices/2/volume",
        json={"volume": 70},
        headers=auth_headers
    )

    assert response.status_code == 200

    device = db_client.get_device_by_id(2)

    assert device is not None
    assert device["volume"] == 70


@pytest.mark.db
def test_washing_machine_water_level_updated_in_database(api_client, auth_headers, db_client):
    response = api_client.patch(
        "/api/devices/4/cycle",
        json={"water_level": 5},
        headers=auth_headers
    )

    assert response.status_code == 200

    device = db_client.get_device_by_id(4)

    assert device is not None
    assert device["water_level"] == 5


@pytest.mark.db
def test_audit_log_created_after_ac_temperature_update(api_client, auth_headers, db_client):
    response = api_client.patch(
        "/api/devices/1/temperature",
        json={"temperature": 26},
        headers=auth_headers
    )

    assert response.status_code == 200

    latest_log = db_client.get_latest_audit_log_by_device(1)

    assert latest_log is not None
    assert latest_log["action"] == "TEMPERATURE_CHANGED"
    assert latest_log["new_value"] == "26"