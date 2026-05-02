import pytest


@pytest.mark.api
@pytest.mark.boundary
@pytest.mark.parametrize("temperature, expected_status", [
    (15, 400),
    (16, 200),
    (17, 200),
    (30, 200),
    (31, 400),
])
def test_ac_temperature_boundary(api_client, auth_headers, temperature, expected_status):
    response = api_client.patch(
        "/api/devices/1/temperature",
        json={"temperature": temperature},
        headers=auth_headers
    )

    assert response.status_code == expected_status


@pytest.mark.api
@pytest.mark.boundary
@pytest.mark.parametrize("volume, expected_status", [
    (-1, 400),
    (0, 200),
    (50, 200),
    (100, 200),
    (101, 400),
])
def test_tv_volume_boundary(api_client, auth_headers, volume, expected_status):
    response = api_client.patch(
        "/api/devices/2/volume",
        json={"volume": volume},
        headers=auth_headers
    )

    assert response.status_code == expected_status


@pytest.mark.api
@pytest.mark.boundary
@pytest.mark.parametrize("temperature, expected_status", [
    (0, 400),
    (1, 200),
    (4, 200),
    (8, 200),
    (9, 400),
])
def test_refrigerator_temperature_boundary(api_client, auth_headers, temperature, expected_status):
    response = api_client.patch(
        "/api/devices/3/temperature",
        json={"temperature": temperature},
        headers=auth_headers
    )

    assert response.status_code == expected_status


@pytest.mark.api
@pytest.mark.boundary
@pytest.mark.parametrize("water_level, expected_status", [
    (0, 400),
    (1, 200),
    (3, 200),
    (5, 200),
    (6, 400),
])
def test_washing_machine_water_level_boundary(api_client, auth_headers, water_level, expected_status):
    response = api_client.patch(
        "/api/devices/4/cycle",
        json={"water_level": water_level},
        headers=auth_headers
    )

    assert response.status_code == expected_status