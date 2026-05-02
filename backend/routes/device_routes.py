from flask import Blueprint, jsonify, request
from services.auth_service import validate_token
from services.device_service import (
    get_all_devices,
    get_device_by_id,
    update_device_power,
    update_device_temperature,
    update_device_volume,
    update_device_mode,
    update_washing_machine_cycle
)

device_bp = Blueprint("devices", __name__, url_prefix="/api/devices")


def get_current_user():
    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.replace("Bearer ", "")
    return validate_token(token)


@device_bp.route("", methods=["GET"])
def devices():
    user = get_current_user()

    if user is None:
        return jsonify({
            "message": "Unauthorized. Valid token required."
        }), 401

    return jsonify({
        "devices": get_all_devices()
    }), 200


@device_bp.route("/<int:device_id>", methods=["GET"])
def device_detail(device_id):
    user = get_current_user()

    if user is None:
        return jsonify({
            "message": "Unauthorized. Valid token required."
        }), 401

    device = get_device_by_id(device_id)

    if device is None:
        return jsonify({
            "message": "Device not found"
        }), 404

    return jsonify({
        "device": device
    }), 200


@device_bp.route("/<int:device_id>/power", methods=["PATCH"])
def update_power(device_id):
    user = get_current_user()

    if user is None:
        return jsonify({
            "message": "Unauthorized. Valid token required."
        }), 401

    data = request.get_json() or {}
    power = data.get("power")

    device, error = update_device_power(device_id, power)

    if error:
        status_code = 404 if error == "Device not found" else 400
        return jsonify({"message": error}), status_code

    return jsonify({
        "message": "Power updated successfully",
        "device": device
    }), 200


@device_bp.route("/<int:device_id>/temperature", methods=["PATCH"])
def update_temperature(device_id):
    user = get_current_user()

    if user is None:
        return jsonify({
            "message": "Unauthorized. Valid token required."
        }), 401

    data = request.get_json() or {}
    temperature = data.get("temperature")
    freezer_temperature = data.get("freezer_temperature")

    device, error = update_device_temperature(
        device_id,
        temperature,
        freezer_temperature
    )

    if error:
        status_code = 404 if error == "Device not found" else 400
        return jsonify({"message": error}), status_code

    return jsonify({
        "message": "Temperature updated successfully",
        "device": device
    }), 200


@device_bp.route("/<int:device_id>/volume", methods=["PATCH"])
def update_volume(device_id):
    user = get_current_user()

    if user is None:
        return jsonify({
            "message": "Unauthorized. Valid token required."
        }), 401

    data = request.get_json() or {}
    volume = data.get("volume")

    device, error = update_device_volume(device_id, volume)

    if error:
        status_code = 404 if error == "Device not found" else 400
        return jsonify({"message": error}), status_code

    return jsonify({
        "message": "Volume updated successfully",
        "device": device
    }), 200


@device_bp.route("/<int:device_id>/mode", methods=["PATCH"])
def update_mode(device_id):
    user = get_current_user()

    if user is None:
        return jsonify({
            "message": "Unauthorized. Valid token required."
        }), 401

    data = request.get_json() or {}
    mode = data.get("mode")

    device, error = update_device_mode(device_id, mode)

    if error:
        status_code = 404 if error == "Device not found" else 400
        return jsonify({"message": error}), status_code

    return jsonify({
        "message": "Mode updated successfully",
        "device": device
    }), 200


@device_bp.route("/<int:device_id>/cycle", methods=["PATCH"])
def update_cycle(device_id):
    user = get_current_user()

    if user is None:
        return jsonify({
            "message": "Unauthorized. Valid token required."
        }), 401

    data = request.get_json() or {}
    cycle_status = data.get("cycle_status")
    water_level = data.get("water_level")

    device, error = update_washing_machine_cycle(
        device_id,
        cycle_status,
        water_level
    )

    if error:
        status_code = 404 if error == "Device not found" else 400
        return jsonify({"message": error}), status_code

    return jsonify({
        "message": "Washing machine cycle updated successfully",
        "device": device
    }), 200