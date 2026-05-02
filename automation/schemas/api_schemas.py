LOGIN_SUCCESS_SCHEMA = {
    "type": "object",
    "required": ["message", "token", "user"],
    "properties": {
        "message": {"type": "string"},
        "token": {"type": "string"},
        "user": {
            "type": "object",
            "required": ["id", "name", "email", "role"],
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": "string"},
                "role": {"type": "string"}
            }
        }
    }
}


ERROR_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["message"],
    "properties": {
        "message": {"type": "string"}
    }
}


DEVICE_SCHEMA = {
    "type": "object",
    "required": [
        "id",
        "name",
        "type",
        "status",
        "power",
        "firmware_version",
        "owner_id"
    ],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "type": {"type": "string"},
        "status": {"type": "string"},
        "power": {"type": "string"},
        "temperature": {"type": ["integer", "null"]},
        "freezer_temperature": {"type": ["integer", "null"]},
        "volume": {"type": ["integer", "null"]},
        "mode": {"type": ["string", "null"]},
        "cycle_status": {"type": ["string", "null"]},
        "water_level": {"type": ["integer", "null"]},
        "firmware_version": {"type": "string"},
        "health_status": {"type": ["string", "null"]},
        "error_code": {"type": ["string", "null"]},
        "wifi_signal": {"type": ["string", "null"]},
        "owner_id": {"type": "integer"}
    }
}


DEVICES_LIST_SCHEMA = {
    "type": "object",
    "required": ["devices"],
    "properties": {
        "devices": {
            "type": "array",
            "items": DEVICE_SCHEMA
        }
    }
}


DEVICE_DETAIL_SCHEMA = {
    "type": "object",
    "required": ["device"],
    "properties": {
        "device": DEVICE_SCHEMA
    }
}


DEVICE_UPDATE_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["message", "device"],
    "properties": {
        "message": {"type": "string"},
        "device": DEVICE_SCHEMA
    }
}


AUDIT_LOG_SCHEMA = {
    "type": "object",
    "required": [
        "id",
        "device_id",
        "device_name",
        "action",
        "old_value",
        "new_value",
        "message",
        "created_at"
    ],
    "properties": {
        "id": {"type": "integer"},
        "device_id": {"type": ["integer", "null"]},
        "device_name": {"type": ["string", "null"]},
        "action": {"type": "string"},
        "old_value": {"type": ["string", "null"]},
        "new_value": {"type": ["string", "null"]},
        "message": {"type": ["string", "null"]},
        "created_at": {"type": "string"}
    }
}


AUDIT_LOGS_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["audit_logs"],
    "properties": {
        "audit_logs": {
            "type": "array",
            "items": AUDIT_LOG_SCHEMA
        }
    }
}


FIRMWARE_LATEST_SCHEMA = {
    "type": "object",
    "required": ["firmware"],
    "properties": {
        "firmware": {
            "type": "object",
            "required": ["device_type", "latest_firmware_version"],
            "properties": {
                "device_type": {"type": "string"},
                "latest_firmware_version": {"type": "string"}
            }
        }
    }
}


DEVICE_FIRMWARE_SCHEMA = {
    "type": "object",
    "required": ["firmware"],
    "properties": {
        "firmware": {
            "type": "object",
            "required": [
                "device_id",
                "device_name",
                "device_type",
                "current_firmware_version",
                "latest_firmware_version",
                "is_latest"
            ],
            "properties": {
                "device_id": {"type": "integer"},
                "device_name": {"type": "string"},
                "device_type": {"type": "string"},
                "current_firmware_version": {"type": "string"},
                "latest_firmware_version": {"type": "string"},
                "is_latest": {"type": "boolean"}
            }
        }
    }
}


FIRMWARE_UPDATE_SCHEMA = {
    "type": "object",
    "required": ["firmware"],
    "properties": {
        "firmware": {
            "type": "object",
            "required": [
                "device_id",
                "device_name",
                "device_type",
                "firmware_version",
                "message"
            ],
            "properties": {
                "device_id": {"type": "integer"},
                "device_name": {"type": "string"},
                "device_type": {"type": "string"},
                "firmware_version": {"type": "string"},
                "message": {"type": "string"}
            }
        }
    }
}


HEALTH_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["health"],
    "properties": {
        "health": {
            "type": "object",
            "required": [
                "device_id",
                "device_name",
                "device_type",
                "status",
                "health_status",
                "error_code",
                "wifi_signal",
                "firmware_version",
                "latest_firmware_version",
                "firmware_outdated"
            ],
            "properties": {
                "device_id": {"type": "integer"},
                "device_name": {"type": "string"},
                "device_type": {"type": "string"},
                "status": {"type": "string"},
                "health_status": {"type": "string"},
                "error_code": {"type": ["string", "null"]},
                "wifi_signal": {"type": "string"},
                "firmware_version": {"type": "string"},
                "latest_firmware_version": {"type": "string"},
                "firmware_outdated": {"type": "boolean"}
            }
        }
    }
}


HEALTH_ACTION_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["message", "health"],
    "properties": {
        "message": {"type": "string"},
        "health": HEALTH_RESPONSE_SCHEMA["properties"]["health"]
    }
}