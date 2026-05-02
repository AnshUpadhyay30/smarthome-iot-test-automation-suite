from database import get_db_connection
from services.device_service import get_device_by_id
from services.firmware_service import LATEST_FIRMWARE
from services.audit_service import create_audit_log


VALID_ERROR_TYPES = {
    "LOW_WIFI": {
        "health_status": "WARNING",
        "error_code": "E101",
        "wifi_signal": "LOW",
        "message": "Low Wi-Fi signal detected"
    },
    "SENSOR_FAILURE": {
        "health_status": "CRITICAL",
        "error_code": "E202",
        "wifi_signal": "GOOD",
        "message": "Sensor failure detected"
    },
    "OFFLINE": {
        "health_status": "OFFLINE",
        "error_code": "E303",
        "wifi_signal": "NONE",
        "message": "Device is offline"
    }
}


def get_device_health(device_id):
    device = get_device_by_id(device_id)

    if device is None:
        return None, "Device not found"

    latest_firmware = LATEST_FIRMWARE.get(device["type"])
    firmware_outdated = device["firmware_version"] != latest_firmware

    health_status = device.get("health_status") or "HEALTHY"

    if firmware_outdated and health_status == "HEALTHY":
        health_status = "FIRMWARE_OUTDATED"

    return {
        "device_id": device["id"],
        "device_name": device["name"],
        "device_type": device["type"],
        "status": device["status"],
        "health_status": health_status,
        "error_code": device.get("error_code"),
        "wifi_signal": device.get("wifi_signal") or "GOOD",
        "firmware_version": device["firmware_version"],
        "latest_firmware_version": latest_firmware,
        "firmware_outdated": firmware_outdated
    }, None


def simulate_device_error(device_id, error_type):
    if error_type not in VALID_ERROR_TYPES:
        return None, "Unsupported error type"

    conn = get_db_connection()
    row = conn.execute(
        "SELECT * FROM devices WHERE id = ?",
        (device_id,)
    ).fetchone()

    if row is None:
        conn.close()
        return None, "Device not found"

    error_config = VALID_ERROR_TYPES[error_type]

    new_status = "OFFLINE" if error_type == "OFFLINE" else row["status"]

    conn.execute(
        """
        UPDATE devices
        SET health_status = ?, error_code = ?, wifi_signal = ?, status = ?
        WHERE id = ?
        """,
        (
            error_config["health_status"],
            error_config["error_code"],
            error_config["wifi_signal"],
            new_status,
            device_id
        )
    )

    conn.commit()
    conn.close()

    create_audit_log(
        device_id,
        "DEVICE_ERROR_SIMULATED",
        row["health_status"] if "health_status" in row.keys() else "HEALTHY",
        error_config["health_status"],
        f"{row['name']} error simulated: {error_type}"
    )

    return get_device_health(device_id)[0], None


def clear_device_error(device_id):
    conn = get_db_connection()
    row = conn.execute(
        "SELECT * FROM devices WHERE id = ?",
        (device_id,)
    ).fetchone()

    if row is None:
        conn.close()
        return None, "Device not found"

    old_health = row["health_status"] if "health_status" in row.keys() else "HEALTHY"

    conn.execute(
        """
        UPDATE devices
        SET health_status = 'HEALTHY',
            error_code = NULL,
            wifi_signal = 'GOOD',
            status = 'ONLINE'
        WHERE id = ?
        """,
        (device_id,)
    )

    conn.commit()
    conn.close()

    create_audit_log(
        device_id,
        "DEVICE_ERROR_CLEARED",
        old_health,
        "HEALTHY",
        f"{row['name']} error cleared"
    )

    return get_device_health(device_id)[0], None