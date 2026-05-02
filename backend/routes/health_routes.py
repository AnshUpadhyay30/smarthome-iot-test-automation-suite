from flask import Blueprint, jsonify, request
from services.auth_service import validate_token
from services.health_service import (
    get_device_health,
    simulate_device_error,
    clear_device_error
)

health_bp = Blueprint("health", __name__, url_prefix="/api/devices")


def get_current_user():
    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.replace("Bearer ", "")
    return validate_token(token)


@health_bp.route("/<int:device_id>/health", methods=["GET"])
def device_health(device_id):
    user = get_current_user()

    if user is None:
        return jsonify({
            "message": "Unauthorized. Valid token required."
        }), 401

    health, error = get_device_health(device_id)

    if error:
        return jsonify({"message": error}), 404

    return jsonify({
        "health": health
    }), 200


@health_bp.route("/<int:device_id>/simulate-error", methods=["POST"])
def simulate_error(device_id):
    user = get_current_user()

    if user is None:
        return jsonify({
            "message": "Unauthorized. Valid token required."
        }), 401

    data = request.get_json() or {}
    error_type = data.get("error_type")

    health, error = simulate_device_error(device_id, error_type)

    if error:
        status_code = 404 if error == "Device not found" else 400
        return jsonify({"message": error}), status_code

    return jsonify({
        "message": "Device error simulated successfully",
        "health": health
    }), 200


@health_bp.route("/<int:device_id>/clear-error", methods=["POST"])
def clear_error(device_id):
    user = get_current_user()

    if user is None:
        return jsonify({
            "message": "Unauthorized. Valid token required."
        }), 401

    health, error = clear_device_error(device_id)

    if error:
        return jsonify({"message": error}), 404

    return jsonify({
        "message": "Device error cleared successfully",
        "health": health
    }), 200