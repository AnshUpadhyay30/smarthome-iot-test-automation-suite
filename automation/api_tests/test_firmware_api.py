import pytest


@pytest.mark.api
def test_get_latest_ac_firmware(api_client, auth_headers):
    response = api_client.get(
        "/api/firmware/latest/AC",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()

    assert data["firmware"]["device_type"] == "AC"
    assert data["firmware"]["latest_firmware_version"] == "1.1.0"


@pytest.mark.api
def test_get_latest_tv_firmware(api_client, auth_headers):
    response = api_client.get(
        "/api/firmware/latest/TV",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()

    assert data["firmware"]["device_type"] == "TV"
    assert data["firmware"]["latest_firmware_version"] == "1.2.0"


@pytest.mark.api
def test_get_latest_refrigerator_firmware(api_client, auth_headers):
    response = api_client.get(
        "/api/firmware/latest/REFRIGERATOR",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()

    assert data["firmware"]["device_type"] == "REFRIGERATOR"
    assert data["firmware"]["latest_firmware_version"] == "1.1.5"


@pytest.mark.api
def test_get_latest_washing_machine_firmware(api_client, auth_headers):
    response = api_client.get(
        "/api/firmware/latest/WASHING_MACHINE",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()

    assert data["firmware"]["device_type"] == "WASHING_MACHINE"
    assert data["firmware"]["latest_firmware_version"] == "1.0.8"


@pytest.mark.api
@pytest.mark.negative
def test_get_latest_firmware_unsupported_device_type(api_client, auth_headers):
    response = api_client.get(
        "/api/firmware/latest/MICROWAVE",
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json()["message"] == "Unsupported device type"


@pytest.mark.api
@pytest.mark.negative
def test_get_latest_firmware_without_token(api_client):
    response = api_client.get("/api/firmware/latest/AC")

    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized. Valid token required."


@pytest.mark.api
def test_get_device_firmware_success(api_client, auth_headers):
    response = api_client.get(
        "/api/devices/1/firmware",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()

    assert data["firmware"]["device_id"] == 1
    assert data["firmware"]["device_type"] == "AC"
    assert "current_firmware_version" in data["firmware"]
    assert "latest_firmware_version" in data["firmware"]
    assert "is_latest" in data["firmware"]


@pytest.mark.api
@pytest.mark.negative
def test_get_firmware_invalid_device_id(api_client, auth_headers):
    response = api_client.get(
        "/api/devices/999/firmware",
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json()["message"] == "Device not found"


@pytest.mark.api
def test_update_ac_firmware_success(api_client, auth_headers):
    response = api_client.post(
        "/api/devices/1/firmware/update",
        json={"firmware_version": "1.1.0"},
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()

    assert data["firmware"]["device_id"] == 1
    assert data["firmware"]["firmware_version"] == "1.1.0"


@pytest.mark.api
def test_update_tv_firmware_success(api_client, auth_headers):
    response = api_client.post(
        "/api/devices/2/firmware/update",
        json={"firmware_version": "1.2.0"},
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()

    assert data["firmware"]["device_id"] == 2
    assert data["firmware"]["firmware_version"] == "1.2.0"


@pytest.mark.api
@pytest.mark.negative
def test_update_firmware_invalid_format(api_client, auth_headers):
    response = api_client.post(
        "/api/devices/1/firmware/update",
        json={"firmware_version": "v2"},
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json()["message"] == "Invalid firmware version format. Use format x.y.z"


@pytest.mark.api
@pytest.mark.negative
def test_update_firmware_higher_than_supported(api_client, auth_headers):
    response = api_client.post(
        "/api/devices/1/firmware/update",
        json={"firmware_version": "9.9.9"},
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json()["message"] == "Firmware version cannot be higher than latest supported version"


@pytest.mark.api
@pytest.mark.negative
def test_update_firmware_invalid_device_id(api_client, auth_headers):
    response = api_client.post(
        "/api/devices/999/firmware/update",
        json={"firmware_version": "1.1.0"},
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json()["message"] == "Device not found"


@pytest.mark.api
@pytest.mark.negative
def test_update_firmware_without_token(api_client):
    response = api_client.post(
        "/api/devices/1/firmware/update",
        json={"firmware_version": "1.1.0"}
    )

    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized. Valid token required."