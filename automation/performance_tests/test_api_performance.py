import time
import pytest


def assert_response_time_under(response_time_ms, threshold_ms):
    assert response_time_ms < threshold_ms, (
        f"Response time {response_time_ms:.2f}ms exceeded threshold {threshold_ms}ms"
    )


def measure_response_time(api_call):
    start_time = time.perf_counter()
    response = api_call()
    end_time = time.perf_counter()

    response_time_ms = (end_time - start_time) * 1000
    return response, response_time_ms


@pytest.mark.performance
def test_login_api_response_time(api_client):
    response, response_time_ms = measure_response_time(
        lambda: api_client.post(
            "/api/auth/login",
            json={
                "email": "admin@test.com",
                "password": "admin123"
            }
        )
    )

    assert response.status_code == 200
    assert_response_time_under(response_time_ms, 700)


@pytest.mark.performance
def test_devices_list_api_response_time(api_client, auth_headers):
    response, response_time_ms = measure_response_time(
        lambda: api_client.get(
            "/api/devices",
            headers=auth_headers
        )
    )

    assert response.status_code == 200
    assert_response_time_under(response_time_ms, 700)


@pytest.mark.performance
def test_device_detail_api_response_time(api_client, auth_headers):
    response, response_time_ms = measure_response_time(
        lambda: api_client.get(
            "/api/devices/1",
            headers=auth_headers
        )
    )

    assert response.status_code == 200
    assert_response_time_under(response_time_ms, 700)


@pytest.mark.performance
def test_ac_temperature_update_response_time(api_client, auth_headers):
    response, response_time_ms = measure_response_time(
        lambda: api_client.patch(
            "/api/devices/1/temperature",
            json={"temperature": 24},
            headers=auth_headers
        )
    )

    assert response.status_code == 200
    assert_response_time_under(response_time_ms, 800)


@pytest.mark.performance
def test_tv_volume_update_response_time(api_client, auth_headers):
    response, response_time_ms = measure_response_time(
        lambda: api_client.patch(
            "/api/devices/2/volume",
            json={"volume": 45},
            headers=auth_headers
        )
    )

    assert response.status_code == 200
    assert_response_time_under(response_time_ms, 800)


@pytest.mark.performance
def test_audit_logs_api_response_time(api_client, auth_headers):
    response, response_time_ms = measure_response_time(
        lambda: api_client.get(
            "/api/audit-logs",
            headers=auth_headers
        )
    )

    assert response.status_code == 200
    assert_response_time_under(response_time_ms, 900)


@pytest.mark.performance
def test_firmware_latest_api_response_time(api_client, auth_headers):
    response, response_time_ms = measure_response_time(
        lambda: api_client.get(
            "/api/firmware/latest/AC",
            headers=auth_headers
        )
    )

    assert response.status_code == 200
    assert_response_time_under(response_time_ms, 700)


@pytest.mark.performance
def test_device_health_api_response_time(api_client, auth_headers):
    response, response_time_ms = measure_response_time(
        lambda: api_client.get(
            "/api/devices/1/health",
            headers=auth_headers
        )
    )

    assert response.status_code == 200
    assert_response_time_under(response_time_ms, 700)