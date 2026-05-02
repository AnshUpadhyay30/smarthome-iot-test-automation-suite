from database import get_db_connection
from services.audit_service import create_audit_log


def row_to_device(row):
    return {
        "id": row["id"],
        "name": row["name"],
        "type": row["type"],
        "status": row["status"],
        "power": row["power"],
        "temperature": row["temperature"],
        "freezer_temperature": row["freezer_temperature"],
        "volume": row["volume"],
        "mode": row["mode"],
        "cycle_status": row["cycle_status"],
        "water_level": row["water_level"],
        "firmware_version": row["firmware_version"],
        "owner_id": row["owner_id"]
    }


def get_all_devices():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM devices").fetchall()
    conn.close()

    return [row_to_device(row) for row in rows]


def get_device_by_id(device_id):
    conn = get_db_connection()
    row = conn.execute(
        "SELECT * FROM devices WHERE id = ?",
        (device_id,)
    ).fetchone()
    conn.close()

    if row is None:
        return None

    return row_to_device(row)


def update_device_power(device_id, power):
    if power not in ["ON", "OFF"]:
        return None, "Power must be ON or OFF"

    conn = get_db_connection()
    row = conn.execute(
        "SELECT * FROM devices WHERE id = ?",
        (device_id,)
    ).fetchone()

    if row is None:
        conn.close()
        return None, "Device not found"

    if row["status"] == "OFFLINE":
        conn.close()
        return None, "Offline device cannot be controlled"

    old_power = row["power"]

    conn.execute(
        "UPDATE devices SET power = ? WHERE id = ?",
        (power, device_id)
    )
    conn.commit()
    conn.close()

    create_audit_log(
        device_id,
        "POWER_CHANGED",
        old_power,
        power,
        f"{row['name']} power changed from {old_power} to {power}"
    )

    return get_device_by_id(device_id), None


def update_device_temperature(device_id, temperature, freezer_temperature=None):
    conn = get_db_connection()
    row = conn.execute(
        "SELECT * FROM devices WHERE id = ?",
        (device_id,)
    ).fetchone()

    if row is None:
        conn.close()
        return None, "Device not found"

    if row["status"] == "OFFLINE":
        conn.close()
        return None, "Offline device cannot be controlled"

    device_type = row["type"]

    if device_type == "AC":
        if temperature is None:
            conn.close()
            return None, "Temperature is required for AC"

        if temperature < 16 or temperature > 30:
            conn.close()
            return None, "AC temperature must be between 16 and 30"

        old_value = row["temperature"]

        conn.execute(
            "UPDATE devices SET temperature = ? WHERE id = ?",
            (temperature, device_id)
        )
        conn.commit()
        conn.close()

        create_audit_log(
            device_id,
            "TEMPERATURE_CHANGED",
            old_value,
            temperature,
            f"{row['name']} temperature changed from {old_value} to {temperature}"
        )

        return get_device_by_id(device_id), None

    if device_type == "REFRIGERATOR":
        updated = False

        if temperature is not None:
            if temperature < 1 or temperature > 8:
                conn.close()
                return None, "Refrigerator temperature must be between 1 and 8"

            old_value = row["temperature"]

            conn.execute(
                "UPDATE devices SET temperature = ? WHERE id = ?",
                (temperature, device_id)
            )
            conn.commit()
            updated = True

            create_audit_log(
                device_id,
                "FRIDGE_TEMPERATURE_CHANGED",
                old_value,
                temperature,
                f"{row['name']} fridge temperature changed from {old_value} to {temperature}"
            )

        if freezer_temperature is not None:
            if freezer_temperature < -24 or freezer_temperature > -15:
                conn.close()
                return None, "Freezer temperature must be between -24 and -15"

            old_freezer_value = row["freezer_temperature"]

            conn.execute(
                "UPDATE devices SET freezer_temperature = ? WHERE id = ?",
                (freezer_temperature, device_id)
            )
            conn.commit()
            updated = True

            create_audit_log(
                device_id,
                "FREEZER_TEMPERATURE_CHANGED",
                old_freezer_value,
                freezer_temperature,
                f"{row['name']} freezer temperature changed from {old_freezer_value} to {freezer_temperature}"
            )

        conn.close()

        if not updated:
            return None, "Temperature or freezer_temperature is required for Refrigerator"

        return get_device_by_id(device_id), None

    conn.close()
    return None, "Temperature control is only available for AC and Refrigerator"


def update_device_volume(device_id, volume):
    if volume is None:
        return None, "Volume is required"

    if volume < 0 or volume > 100:
        return None, "TV volume must be between 0 and 100"

    conn = get_db_connection()
    row = conn.execute(
        "SELECT * FROM devices WHERE id = ?",
        (device_id,)
    ).fetchone()

    if row is None:
        conn.close()
        return None, "Device not found"

    if row["type"] != "TV":
        conn.close()
        return None, "Volume control is only available for TV"

    if row["status"] == "OFFLINE":
        conn.close()
        return None, "Offline device cannot be controlled"

    old_volume = row["volume"]

    conn.execute(
        "UPDATE devices SET volume = ? WHERE id = ?",
        (volume, device_id)
    )
    conn.commit()
    conn.close()

    create_audit_log(
        device_id,
        "VOLUME_CHANGED",
        old_volume,
        volume,
        f"{row['name']} volume changed from {old_volume} to {volume}"
    )

    return get_device_by_id(device_id), None


def update_device_mode(device_id, mode):
    if not mode:
        return None, "Mode is required"

    conn = get_db_connection()
    row = conn.execute(
        "SELECT * FROM devices WHERE id = ?",
        (device_id,)
    ).fetchone()

    if row is None:
        conn.close()
        return None, "Device not found"

    if row["status"] == "OFFLINE":
        conn.close()
        return None, "Offline device cannot be controlled"

    allowed_modes = {
        "AC": ["COOL", "HEAT", "FAN", "AUTO"],
        "TV": ["HDMI", "AV", "OTT"],
        "REFRIGERATOR": ["ECO", "NORMAL", "POWER_COOL"],
        "WASHING_MACHINE": ["NORMAL", "QUICK", "HEAVY", "DELICATE"]
    }

    device_type = row["type"]

    if mode not in allowed_modes.get(device_type, []):
        conn.close()
        return None, f"Invalid mode for {device_type}"

    old_mode = row["mode"]

    conn.execute(
        "UPDATE devices SET mode = ? WHERE id = ?",
        (mode, device_id)
    )
    conn.commit()
    conn.close()

    create_audit_log(
        device_id,
        "MODE_CHANGED",
        old_mode,
        mode,
        f"{row['name']} mode changed from {old_mode} to {mode}"
    )

    return get_device_by_id(device_id), None


def update_washing_machine_cycle(device_id, cycle_status=None, water_level=None):
    conn = get_db_connection()
    row = conn.execute(
        "SELECT * FROM devices WHERE id = ?",
        (device_id,)
    ).fetchone()

    if row is None:
        conn.close()
        return None, "Device not found"

    if row["type"] != "WASHING_MACHINE":
        conn.close()
        return None, "Cycle control is only available for Washing Machine"

    if row["status"] == "OFFLINE":
        conn.close()
        return None, "Offline device cannot be controlled"

    updated = False

    if cycle_status is not None:
        allowed_cycles = ["START", "PAUSE", "STOP", "IDLE"]

        if cycle_status not in allowed_cycles:
            conn.close()
            return None, "Invalid washing machine cycle status"

        old_cycle = row["cycle_status"]

        conn.execute(
            "UPDATE devices SET cycle_status = ? WHERE id = ?",
            (cycle_status, device_id)
        )
        conn.commit()
        updated = True

        create_audit_log(
            device_id,
            "CYCLE_STATUS_CHANGED",
            old_cycle,
            cycle_status,
            f"{row['name']} cycle changed from {old_cycle} to {cycle_status}"
        )

    if water_level is not None:
        if water_level < 1 or water_level > 5:
            conn.close()
            return None, "Water level must be between 1 and 5"

        old_water_level = row["water_level"]

        conn.execute(
            "UPDATE devices SET water_level = ? WHERE id = ?",
            (water_level, device_id)
        )
        conn.commit()
        updated = True

        create_audit_log(
            device_id,
            "WATER_LEVEL_CHANGED",
            old_water_level,
            water_level,
            f"{row['name']} water level changed from {old_water_level} to {water_level}"
        )

    conn.close()

    if not updated:
        return None, "cycle_status or water_level is required"

    return get_device_by_id(device_id), None