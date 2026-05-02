from flask import Blueprint, jsonify, request
from services.auth_service import validate_token
from services.firmware_service import (
    get_latest_firmware_by_device_type,
    get_device_firmware,
    update_device_firmware
)

firmware_bp = Blueprint("firmware", __name__, url_prefix="/api")


def get_current_user():
    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.replace("Bearer ", "")
    return validate_token(token)


@firmware_bp.route("/firmware/latest/<device_type>", methods=["GET"])
def latest_firmware(device_type):
    user = get_current_user()

    if user is None:
        return jsonify({
            "message": "Unauthorized. Valid token required."
        }), 401

    firmware, error = get_latest_firmware_by_device_type(device_type)

    if error:
        return jsonify({"message": error}), 400

    return jsonify({
        "firmware": firmware
    }), 200


@firmware_bp.route("/devices/<int:device_id>/firmware", methods=["GET"])
def device_firmware(device_id):
    user = get_current_user()

    if user is None:
        return jsonify({
            "message": "Unauthorized. Valid token required."
        }), 401

    firmware, error = get_device_firmware(device_id)

    if error:
        status_code = 404 if error == "Device not found" else 400
        return jsonify({"message": error}), status_code

    return jsonify({
        "firmware": firmware
    }), 200


@firmware_bp.route("/devices/<int:device_id>/firmware/update", methods=["POST"])
def update_firmware(device_id):
    user = get_current_user()

    if user is None:
        return jsonify({
            "message": "Unauthorized. Valid token required."
        }), 401

    data = request.get_json() or {}
    new_version = data.get("firmware_version")

    firmware, error = update_device_firmware(device_id, new_version)

    if error:
        status_code = 404 if error == "Device not found" else 400
        return jsonify({"message": error}), status_code

    return jsonify({
        "firmware": firmware
    }), 200