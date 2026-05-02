import re
from database import get_db_connection
from services.device_service import get_device_by_id
from services.audit_service import create_audit_log


LATEST_FIRMWARE = {
    "AC": "1.1.0",
    "TV": "1.2.0",
    "REFRIGERATOR": "1.1.5",
    "WASHING_MACHINE": "1.0.8"
}


def is_valid_version(version):
    if not version:
        return False

    pattern = r"^\d+\.\d+\.\d+$"
    return re.match(pattern, version) is not None


def version_to_tuple(version):
    return tuple(map(int, version.split(".")))


def get_latest_firmware_by_device_type(device_type):
    device_type = device_type.upper()

    latest_version = LATEST_FIRMWARE.get(device_type)

    if latest_version is None:
        return None, "Unsupported device type"

    return {
        "device_type": device_type,
        "latest_firmware_version": latest_version
    }, None


def get_device_firmware(device_id):
    device = get_device_by_id(device_id)

    if device is None:
        return None, "Device not found"

    latest_version = LATEST_FIRMWARE.get(device["type"])
    is_latest = device["firmware_version"] == latest_version

    return {
        "device_id": device["id"],
        "device_name": device["name"],
        "device_type": device["type"],
        "current_firmware_version": device["firmware_version"],
        "latest_firmware_version": latest_version,
        "is_latest": is_latest
    }, None


def update_device_firmware(device_id, new_version):
    if not is_valid_version(new_version):
        return None, "Invalid firmware version format. Use format x.y.z"

    conn = get_db_connection()
    row = conn.execute(
        "SELECT * FROM devices WHERE id = ?",
        (device_id,)
    ).fetchone()

    if row is None:
        conn.close()
        return None, "Device not found"

    device_type = row["type"]
    latest_version = LATEST_FIRMWARE.get(device_type)

    if latest_version is None:
        conn.close()
        return None, "Unsupported device type"

    current_version = row["firmware_version"]

    if version_to_tuple(new_version) < version_to_tuple(current_version):
        conn.close()
        return None, "Firmware downgrade is not allowed"

    if version_to_tuple(new_version) > version_to_tuple(latest_version):
        conn.close()
        return None, "Firmware version cannot be higher than latest supported version"

    if new_version == current_version:
        conn.close()
        return {
            "device_id": row["id"],
            "device_name": row["name"],
            "device_type": row["type"],
            "firmware_version": current_version,
            "message": "Device is already on this firmware version"
        }, None

    conn.execute(
        "UPDATE devices SET firmware_version = ? WHERE id = ?",
        (new_version, device_id)
    )
    conn.commit()
    conn.close()

    create_audit_log(
        device_id,
        "FIRMWARE_UPDATED",
        current_version,
        new_version,
        f"{row['name']} firmware updated from {current_version} to {new_version}"
    )

    updated_device = get_device_by_id(device_id)

    return {
        "device_id": updated_device["id"],
        "device_name": updated_device["name"],
        "device_type": updated_device["type"],
        "firmware_version": updated_device["firmware_version"],
        "message": "Firmware updated successfully"
    }, None