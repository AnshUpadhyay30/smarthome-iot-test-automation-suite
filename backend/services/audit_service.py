from database import get_db_connection


def create_audit_log(device_id, action, old_value, new_value, message):
    conn = get_db_connection()
    conn.execute(
        """
        INSERT INTO audit_logs (device_id, action, old_value, new_value, message)
        VALUES (?, ?, ?, ?, ?)
        """,
        (device_id, action, str(old_value), str(new_value), message)
    )
    conn.commit()
    conn.close()


def get_audit_logs():
    conn = get_db_connection()
    rows = conn.execute(
        """
        SELECT audit_logs.*, devices.name AS device_name
        FROM audit_logs
        LEFT JOIN devices ON audit_logs.device_id = devices.id
        ORDER BY audit_logs.created_at DESC
        """
    ).fetchall()
    conn.close()

    return [
        {
            "id": row["id"],
            "device_id": row["device_id"],
            "device_name": row["device_name"],
            "action": row["action"],
            "old_value": row["old_value"],
            "new_value": row["new_value"],
            "message": row["message"],
            "created_at": row["created_at"]
        }
        for row in rows
    ]