from flask import Blueprint, jsonify, request
from services.auth_service import validate_token
from services.audit_service import get_audit_logs

audit_bp = Blueprint("audit", __name__, url_prefix="/api/audit-logs")


def get_current_user():
    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.replace("Bearer ", "")
    return validate_token(token)


@audit_bp.route("", methods=["GET"])
def audit_logs():
    user = get_current_user()

    if user is None:
        return jsonify({
            "message": "Unauthorized. Valid token required."
        }), 401

    return jsonify({
        "audit_logs": get_audit_logs()
    }), 200